from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv()

# Importez les modules nécessaires
from .helper.response import http_exception_handler, validation_exception_handler
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

# Charger les modèles et créer la base de données...
from .models import user, environment, user_assignment, group, function, group_function,  element, audit_log
from .database.session import engine
from .database.base import Base

Base.metadata.create_all(bind=engine)

# Appel du seeding des fonctions
from .database.seed import seed
from .database.session import SessionLocal

db = SessionLocal()
seed(db)
db.close()
# Import des routeurs
from .api import users, environments, groups, elements, audit_logs

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001"],  # Vue's origin
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

# Enregistrement des routeurs
app.include_router(users.router)
app.include_router(environments.router)
app.include_router(groups.router)
app.include_router(elements.router)
app.include_router(audit_logs.router)

# Enregistrement des gestionnaires d'erreurs globales
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

def main():
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)

if __name__ == "__main__":
    main()
