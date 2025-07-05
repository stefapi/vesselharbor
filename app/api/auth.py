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

from ..helper.security import create_password_reset_token
from ..models.user import User
from ..database.session import SessionLocal
from ..helper import security, audit, email, response
from ..repositories import user_repo
from ..schema.password_reset import PasswordResetRequest, PasswordReset
from ..core import auth
from ..schema.user import UserOut
from ..schema.auth import LoginResponse, LogoutResponse, RefreshTokenResponse, MeResponse, PasswordResetResponse

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
        if authorization and scheme.lower() == "bearer" and param.lower() != 'undefined':
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
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        user = user_repo.get_user(db, int(user_id))
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        return user
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

@router.post("/login", response_model=LoginResponse, summary="Authenticate a user", description="Authenticates a user with their email and password and returns an access token", responses={
    200: {"description": "Login successful"},
    400: {"description": "Incorrect email or password"}
})
def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db), response_item: Response = None):
    ip = request.headers.get("x-forwarded-for", request.client.host if request.client else "unknown").split(",")[0]
    user = user_repo.get_user_by_email(db, form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token = auth.create_token(data={"sub": str(user.id)}, expires_delta=timedelta(minutes=1), token_type="access")
    refresh_token = auth.create_token(data={"sub": str(user.id)}, expires_delta=timedelta(days=7), token_type="refresh")
    audit.log_action(db, user.id, "Login", f"Successful connection from IP {ip}")
    response_item.set_cookie("access_token", access_token, httponly=True, samesite="strict", secure=True, max_age=timedelta(minutes=1).total_seconds())
    response_item.set_cookie("refresh_token", refresh_token, httponly=True, samesite="strict", secure=True, max_age=timedelta(days=7).total_seconds(), path="/")
    return response.success_response({"token_type": "bearer"}, "Login successful")

@router.post("/logout", response_model=LogoutResponse, summary="Log out", description="Logs out the user by deleting authentication cookies", responses={
    200: {"description": "Logout successful"}
})
async def logout(response_item: Response):
    response_item.delete_cookie("access_token")
    response_item.delete_cookie("refresh_token")
    return response.success_response({}, "Logout successful")

@router.post("/refresh-token", response_model=RefreshTokenResponse, summary="Renew token", description="Renews the access token from a valid refresh token", responses={
    200: {"description": "Token renewed successfully"},
    400: {"description": "Invalid or expired refresh token, or is not a refresh token"}
})
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
        raise HTTPException(status_code=400, detail="Invalid or expired refresh token")
    if payload.get("token_type") != "refresh":
        raise HTTPException(status_code=400, detail="The provided token is not a refresh token")
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=400, detail="Invalid refresh token")
    access_token = auth.create_token(data={"sub": str(user_id)}, expires_delta=timedelta(minutes=1), token_type="access")
    response_item.set_cookie("access_token", access_token, httponly=True, samesite="strict", secure=True, max_age=timedelta(minutes=1))
    return response.success_response({"token_type": "access"}, "Token renewed successfully")

@router.get("/me", summary="Connected user profile", description="Retrieves the profile information of the currently connected user", response_model=MeResponse, responses={
    200: {"description": "Profile information retrieved successfully"},
    401: {"description": "Not authenticated or invalid token"}
})
def get_me(current_user: User = Depends(get_current_user)):
    return response.success_response(UserOut.model_validate(current_user), "Profile information")

@router.post("/users/reset_password_request", response_model=PasswordResetResponse, summary="Request password reset", description="Sends an email containing a password reset link to the provided email address", responses={
    200: {"description": "Reset link sent by email (if the email is registered)"}
})
def reset_password_request(reset_req: PasswordResetRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    user = user_repo.get_user_by_email(db, reset_req.email)
    if user:
        token = create_password_reset_token(user.id)
        background_tasks.add_task(email.send_reset_email, user.email, token)
        audit.log_action(db, user.id, "Password reset", "Reset link sent by email")
    return response.success_response(None, "If this email is registered, you will receive a reset link.")

@router.post("/users/reset_password", response_model=PasswordResetResponse, summary="Reset password", description="Resets a user's password using a valid reset token", responses={
    200: {"description": "Password reset successfully"},
    400: {"description": "Invalid, expired or incorrect token"},
    404: {"description": "User not found"}
})
def reset_password(reset: PasswordReset, db: Session = Depends(get_db)):
    try:
        payload = auth.decode_token(reset.token)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    if payload.get("token_type") != "password_reset":
        raise HTTPException(status_code=400, detail="Incorrect token")
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=400, detail="Invalid token")
    user = user_repo.get_user(db, int(user_id))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.hashed_password = security.get_password_hash(reset.new_password)
    db.commit()
    audit.log_action(db, user.id, "Password reset", "Password reset via email link")
    return response.success_response(None, "Password reset successfully")
