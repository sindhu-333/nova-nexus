"""
Authentication routes for Nova Nexus
"""
from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from app.services.auth_service import auth_service
from typing import Optional

router = APIRouter(tags=["auth"])


class LoginRequest(BaseModel):
    """Login request model"""
    email: str
    password: str


class RegisterRequest(BaseModel):
    """User registration request model"""
    username: str
    email: str
    password: str
    role: str = "Operator"


class VerifySessionRequest(BaseModel):
    """Session verification request"""
    token: str


@router.post("/auth/login")
async def login(request: LoginRequest):
    """
    User login endpoint
    
    Args:
        request: Login credentials
        
    Returns:
        Login result with session token
    """
    result = auth_service.login(request.email, request.password)
    
    if not result["success"]:
        # Return error details but don't expose internal structure
        raise HTTPException(
            status_code=401,
            detail={
                "error": result.get("error"),
                "message": result.get("message"),
                "attempts_left": result.get("attempts_left")
            }
        )
    
    return result


@router.post("/auth/logout")
async def logout(authorization: Optional[str] = Header(None)):
    """
    User logout endpoint
    
    Args:
        authorization: Bearer token
        
    Returns:
        Logout confirmation
    """
    if not authorization:
        raise HTTPException(status_code=401, detail="No token provided")
    
    # Extract token from "Bearer <token>"
    token = authorization.split(" ")[-1] if authorization else ""
    result = auth_service.logout(token)
    
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result.get("message"))
    
    return result


@router.post("/auth/verify")
async def verify_session(request: VerifySessionRequest):
    """
    Verify session validity
    
    Args:
        request: Session token
        
    Returns:
        Session validation status
    """
    session = auth_service.verify_session(request.token)
    
    if not session:
        raise HTTPException(status_code=401, detail="Invalid or expired session")
    
    return {
        "success": True,
        "valid": True,
        "session": session
    }


@router.post("/auth/register")
async def register(request: RegisterRequest):
    """
    Register new user endpoint
    
    Args:
        request: Registration data
        
    Returns:
        Registration result
    """
    result = auth_service.register_user(
        request.username,
        request.email,
        request.password,
        request.role
    )
    
    if not result["success"]:
        raise HTTPException(
            status_code=400,
            detail={
                "error": result.get("error"),
                "message": result.get("message")
            }
        )
    
    return result


@router.get("/auth/demo-users")
async def get_demo_users():
    """
    Get list of demo users for testing
    
    Returns:
        List of demo user credentials
    """
    return {
        "demo_users": [
            {
                "email": "operator@factory.com",
                "password": "password",
                "role": "Manufacturing"
            },
            {
                "email": "manager@factory.com",
                "password": "manager123",
                "role": "Supervisor"
            },
            {
                "email": "supervisor@factory.com",
                "password": "supervisor123",
                "role": "Quality Control"
            }
        ]
    }
