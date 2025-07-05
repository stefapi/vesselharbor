# app/schema/auth.py
from pydantic import BaseModel
from typing import Generic, TypeVar, Any, Optional

# Generic type for response data
T = TypeVar('T')

class BaseResponse(BaseModel, Generic[T]):
    """Base response schema that matches the standardized response format"""
    status: str
    message: str
    data: T

class LoginData(BaseModel):
    """Data structure for login response"""
    token_type: str

class LoginResponse(BaseResponse[LoginData]):
    """Response schema for login endpoint"""
    pass

class RefreshTokenData(BaseModel):
    """Data structure for refresh token response"""
    token_type: str

class RefreshTokenResponse(BaseResponse[RefreshTokenData]):
    """Response schema for refresh token endpoint"""
    pass

class EmptyData(BaseModel):
    """Empty data structure for responses with no data"""
    pass

class LogoutResponse(BaseResponse[EmptyData]):
    """Response schema for logout endpoint"""
    pass

class PasswordResetResponse(BaseResponse[Optional[Any]]):
    """Response schema for password reset endpoints"""
    pass

# For the /me endpoint, we'll create a specific response that uses UserOut
from .user import UserOut

class MeResponse(BaseResponse[UserOut]):
    """Response schema for me/profile endpoint"""
    pass

class Token(BaseModel):
    access_token: str
    token_type: str
