#!/usr/bin/env python3
import re
import sys
import unicodedata
from enum import Enum
from itertools import groupby
from pathlib import Path

import slugify
from fastapi import FastAPI
from humps import camelize
from jinja2 import Template
from pydantic import BaseModel, computed_field

# Add the project root to Python path to import from app
CWD = Path(__file__).parent
PROJECT_ROOT = CWD / ".." / ".."
sys.path.insert(0, str(PROJECT_ROOT))

from app.main import app

# Output to frontend/src/api instead of dev/scripts/output/javascriptAPI
TS_DIR = PROJECT_ROOT / "frontend" / "src" / "api"
TS_OUT_FILE = TS_DIR / "apiRoutes.ts"
TEMPLATES_DIR = CWD / ".." / "templates"

TS_REQUESTS = TEMPLATES_DIR / "ts_requests.jinja"
TS_ROUTES = TEMPLATES_DIR / "ts_routes.jinja"
TS_INDEX = TEMPLATES_DIR / "ts_index.jinja"

TS_DIR.mkdir(exist_ok=True, parents=True)


def sanitize_function_name(text: str) -> str:
    """
    Sanitize text to create valid TypeScript function names.
    Removes apostrophes and converts accented characters to their non-accented equivalents.
    """
    if not text:
        return text

    # Remove various types of apostrophes and quotes using Unicode code points
    apostrophe_codes = [0x0027, 0x2018, 0x2019, 0x0060, 0x00B4, 0x02BC, 0x02BB, 0x02BD, 0x02BE, 0x02BF]
    for code in apostrophe_codes:
        char = chr(code)
        if char in text:
            text = text.replace(char, "")

    # Convert accented characters to their non-accented equivalents
    # NFD normalization decomposes characters into base + combining characters
    # Then we filter out the combining characters (category 'Mn')
    text = ''.join(c for c in unicodedata.normalize('NFD', text)
                   if unicodedata.category(c) != 'Mn')
    return text


class RouteObject:
    def __init__(self, route_string) -> None:
        self.prefix = "/" + route_string.split("/")[1]
        self.route = route_string.replace(self.prefix, "")
        self.js_route = self.route.replace("{", "${")
        self.parts = route_string.split("/")[1:]
        self.var = re.findall(r"\{(.*?)\}", route_string)
        self.is_function = "{" in self.route
        # Include all parts to avoid collisions, not just parts[1:]
        self.router_slug = slugify.slugify("_".join(self.parts), separator="_")
        self.router_camel = camelize(self.router_slug)

    def __repr__(self) -> str:
        return f"""Route: {self.route}
Parts: {self.parts}
Function: {self.is_function}
Var: {self.var}
Slug: {self.router_slug}
"""


class RequestType(str, Enum):
    get = "get"
    put = "put"
    post = "post"
    patch = "patch"
    delete = "delete"


class HTTPRequest(BaseModel):
    request_type: RequestType
    description: str = ""
    summary: str = ""
    tags: list[str] = []
    requestBody: dict = {}
    vars: list[str] = []
    @computed_field
    @property
    def content(self)-> str:
        if 'content' in self.requestBody:
            if 'application/json' in self.requestBody['content']:
                a= self.requestBody['content']['application/json']['schema']['$ref'].split("/")[-1]
                return a
        return ""

    @property
    def summary_camel(self):
        camelized = camelize(self.summary)
        result = sanitize_function_name(camelized)
        return result

    @property
    def js_docs(self):
        return self.description.replace("\n", "  \n  * ")


class PathObject(BaseModel):
    route_object: RouteObject
    http_verbs: list[HTTPRequest]

    class Config:
        arbitrary_types_allowed = True


def get_path_objects(app: FastAPI):
    paths = []
    schemas = {}

    for key, value in app.openapi().items():
        if key == "paths":
            for key, value in value.items():
                paths.append(
                    PathObject(
                        route_object=RouteObject(key),
                        http_verbs=[HTTPRequest(request_type=k, **v) for k, v in value.items()],
                    )
                )
        elif key == "components":
            for key, value in value.items():
                if key == "schemas":
                    for key, value in value.items():
                        schemas[key] = [k for k, v in value['properties'].items()]

    for path in paths:
        for verb in path.http_verbs:
            if verb.content in schemas:
                verb.vars = list(schemas[verb.content])
    return paths


def read_template(file: Path):
    with open(file, "r") as f:
        return f.read()


def generate_template(app):
    paths = get_path_objects(app)

    static_paths = [x.route_object for x in paths if not x.route_object.is_function]
    get_paths = [x.route_object for x in paths if x.route_object.is_function]

    static_paths.sort(key=lambda x: x.router_slug)
    get_paths.sort(key=lambda x: x.router_slug)

    template = Template(read_template(TS_ROUTES))
    content = template.render(
        paths={"prefix": paths[0].route_object.prefix, "static_paths": static_paths, "get_paths": get_paths, "all_paths": paths}
    )
    with open(TS_OUT_FILE, "w") as f:
        f.write(content)

    all_tags = []
    for k, g in groupby(paths, lambda x: "_".join(x.http_verbs[0].tags)):
        # Handle endpoints without tags by assigning them to a default category
        if not k or not camelize(k):
            k = "root"  # Default category for endpoints without tags

        # Skip if the camelized name is still empty (shouldn't happen now)
        camelized_name = camelize(k)
        if not camelized_name:
            continue

        template = Template(read_template(TS_REQUESTS))
        content = template.render(paths={"all_paths": list(g), "export_name": camelized_name})

        all_tags.append(camelized_name)

        with open(TS_DIR.joinpath(camelized_name + ".ts"), "w") as f:
            f.write(content)

    template = Template(read_template(TS_INDEX))
    content = template.render(files={"files": all_tags})

    with open(TS_DIR.joinpath("index.ts"), "w") as f:
        f.write(content)


if __name__ == "__main__":
    generate_template(app)
