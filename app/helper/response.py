from fastapi.responses import JSONResponse
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

def success_response(data, message="Success"):
    """
    Retourne une réponse standardisée de succès.
    """
    return {"status": "success", "message": message, "data": data}

def error_response(message, code, detail=None):
    """
    Retourne une réponse standardisée d'erreur.
    """
    return {"status": "error", "message": message, "code": code, "detail": detail}

# Gestionnaire d'exceptions HTTP
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response(str(exc.detail), exc.status_code)
    )

# Gestionnaire d'erreurs de validation
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content=error_response("Validation error", 422, detail=exc.errors())
    )
