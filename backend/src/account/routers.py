from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from src.account.models import User
from src.db.config import SessionDep
from src.account.schemas import PasswordChangeRequest, PasswordResetEmailRequest, PasswordResetRequest, UserCreate, UserOut, UserLogin
from src.account.services import password_reset_email_send, change_password, create_user, authenticate_user, email_verification_send, verify_email_token, verify_password_reset_token
from src.account.utils import create_tokens, verify_refresh_token
from src.account.deps import get_current_user

router = APIRouter()


@router.post("/register", response_model=UserOut)
async def register(session: SessionDep, user: UserCreate):
    return await create_user(session, user)


@router.post("/login")
async def login(session: SessionDep, user_login: UserLogin):
    user = await authenticate_user(session, user_login)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials"
        )

    tokens = await create_tokens(session, user)
    response = JSONResponse(content={"message": "Login Successful"})
    response.set_cookie(
        "access_token",
        value=tokens["access_token"],
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=60 * 60 * 24 * 1,
    )
    response.set_cookie(
        "refresh_token",
        value=tokens["refresh_token"],
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=60 * 60 * 24 * 7,
    )
    return response


@router.get("/me", response_model=UserOut)
async def me(user: User = Depends(get_current_user)):
    return user


@router.post("/refresh")
async def refresh_token(session: SessionDep, request: Request):
    token = request.cookies.get("refresh_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Refresh Token",
        )
    user = await verify_refresh_token(session, token)
    if not user:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail = "Session expired, please login again"
        )
    tokens = await create_tokens(session, user)
    response = JSONResponse(content = {"message": "Token refresh successful"})
    response.set_cookie(
       "access_token",
       value=tokens["access_token"],
       httponly=True,
       secure=False,
       samesite="lax",
       max_age=60 * 60 * 24 * 1,
    )
    response.set_cookie(
        "refresh_token",
        value=tokens["refresh_token"],
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=60 * 60 * 24 * 7,
    )
    return response

@router.post("/send-verification-email")
async def send_verification_email(user: User = Depends(get_current_user)):
    return await email_verification_send(user)

@router.get("/verify-email")
async def verify_email(session: SessionDep, token: str):
    return await verify_email_token(session,token)

@router.post("/change-password")
async def password_change(session: SessionDep, data: PasswordChangeRequest, user: User = Depends(get_current_user)):
    await change_password(session, user, data)
    return {"msg": "Password changed successfully..."}

@router.post("/send-password-reset-email")
async def send_password_reset_email(session: SessionDep, data: PasswordResetEmailRequest):
    return await password_reset_email_send(session, data)

@router.post("/verify-password-reset-token")
async def verify_password_reset_email(session: SessionDep, data: PasswordResetRequest, ):
    return await verify_password_reset_token(session, data)
   