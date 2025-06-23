# app/api/auth.py

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks, Response, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Optional, Dict, cast, Any
from datetime import timedelta
from fastapi.security import OAuth2
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security.utils import get_authorization_scheme_param
from starlette.status import HTTP_401_UNAUTHORIZED

from ..models.user import User
from ..database.session import SessionLocal
from ..helper import security, audit, email, response
from ..repositories import user_repo
from ..schema.password_reset import PasswordResetRequest, PasswordReset
from ..core import auth
from ..schema.user import UserOut

router = APIRouter()

class OAuth2PasswordBearerOrKey(OAuth2):
    def __init__(
        self,
        tokenUrl: str,
        scheme_name: Optional[str] = None,
        scopes: Optional[Dict[str, str]] = None,
        description: Optional[str] = None,
        auto_error: bool = True,
    ):
        flows = OAuthFlowsModel(password=cast(Any, {"tokenUrl": tokenUrl, "scopes": scopes or {}}))
        super().__init__(
            flows=flows,
            scheme_name=scheme_name,
            description=description,
            auto_error=auto_error,
        )

    async def __call__(self, request: Request) -> Optional[str]:
        authorization = request.headers.get("Authorization")
        scheme, param = get_authorization_scheme_param(authorization)
        if authorization and scheme.lower() == "bearer":
            return param
        key = request.cookies.get("access_token")
        key = key or request.headers.get("X-API-KEY")
        key = key or request.cookies.get("X-API-KEY")
        key = key or request.query_params.get("key")
        if not key and self.auto_error:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return key

oauth2_scheme = OAuth2PasswordBearerOrKey(tokenUrl="/login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    try:
        payload = auth.decode_token(token)
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalide")
        user = user_repo.get_user(db, int(user_id))
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Utilisateur non trouvé")
        return user
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Identifiants invalides")

@router.post("/login", response_model=dict, summary="Authentifier un utilisateur")
def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db), response_item: Response = None):
    ip = request.headers.get("x-forwarded-for", request.client.host if request.client else "unknown").split(",")[0]
    user = user_repo.get_user_by_email(db, form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Email ou mot de passe incorrect")
    access_token = auth.create_token(data={"sub": str(user.id)}, expires_delta=timedelta(minutes=1), token_type="access")
    refresh_token = auth.create_token(data={"sub": str(user.id)}, expires_delta=timedelta(days=7), token_type="refresh")
    audit.log_action(db, user.id, "Login", f"Connexion réussie depuis IP {ip}")
    response_item.set_cookie("access_token", access_token, httponly=True, samesite="strict", secure=True, max_age=timedelta(minutes=1).total_seconds())
    response_item.set_cookie("refresh_token", refresh_token, httponly=True, samesite="strict", secure=True, max_age=timedelta(days=7).total_seconds(), path="/")
    return response.success_response({"token_type": "bearer"}, "Login réussi")

@router.post("/logout", response_model=dict, summary="Se déconnecter")
async def logout(response_item: Response):
    response_item.delete_cookie("access_token")
    response_item.delete_cookie("refresh_token")
    return response.success_response({}, "Déconnexion réussie")

@router.post("/refresh-token", response_model=dict, summary="Renouveler le token")
def refresh_token(request: Request, response_item: Response = None, db: Session = Depends(get_db)):
    refresh_token = request.cookies.get("refresh_token")
    if refresh_token is None:
        authorization = request.headers.get("Authorization")
        scheme, param = get_authorization_scheme_param(authorization)
        if authorization and scheme.lower() == "bearer":
            refresh_token = param
    try:
        payload = auth.decode_token(refresh_token)
    except Exception:
        raise HTTPException(status_code=400, detail="Refresh token invalide ou expiré")
    if payload.get("token_type") != "refresh":
        raise HTTPException(status_code=400, detail="Le token fourni n'est pas un refresh token")
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=400, detail="Refresh token invalide")
    access_token = auth.create_token(data={"sub": str(user_id)}, expires_delta=timedelta(minutes=1), token_type="access")
    response_item.set_cookie("access_token", access_token, httponly=True, samesite="strict", secure=True, max_age=timedelta(minutes=1))
    return response.success_response({"token_type": "access"}, "Token renouvelé avec succès")

@router.get("/me", summary="Profil utilisateur connecté", response_model=UserOut)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.post("/users/reset_password_request", response_model=dict, summary="Demander une réinitialisation de mot de passe")
def reset_password_request(reset_req: PasswordResetRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    user = user_repo.get_user_by_email(db, reset_req.email)
    if user:
        token = auth.create_token(data={"sub": str(user.id)}, token_type="password_reset")
        background_tasks.add_task(email.send_reset_email, user.email, token)
        audit.log_action(db, user.id, "Réinitialisation mot de passe", "Lien de réinitialisation envoyé par email")
    return response.success_response(None, "Si cet email est enregistré, vous recevrez un lien de réinitialisation.")

@router.post("/users/reset_password", response_model=dict, summary="Réinitialiser le mot de passe")
def reset_password(reset: PasswordReset, db: Session = Depends(get_db)):
    try:
        payload = auth.decode_token(reset.token)
    except Exception:
        raise HTTPException(status_code=400, detail="Token invalide ou expiré")
    if payload.get("token_type") != "password_reset":
        raise HTTPException(status_code=400, detail="Token incorrect")
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=400, detail="Token invalide")
    user = user_repo.get_user(db, int(user_id))
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    user.hashed_password = security.get_password_hash(reset.new_password)
    db.commit()
    audit.log_action(db, user.id, "Réinitialisation mot de passe", "Mot de passe réinitialisé via lien email")
    return response.success_response(None, "Mot de passe réinitialisé avec succès")
