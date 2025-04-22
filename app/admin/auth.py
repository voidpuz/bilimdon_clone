from fastapi import Request, Response, HTTPException
from starlette_admin.auth import AdminConfig, AdminUser, AuthProvider
from starlette_admin.exceptions import FormValidationError, LoginFailed
from sqlalchemy.orm import Session

from datetime import timedelta, datetime, timezone
from jose import jwt
from typing import Optional

from app.dependencies import get_db
from app.models import User
from app.utils import verify_password, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM



class JSONAuthProvider(AuthProvider):
    async def login(
        self,
        email: str,
        password: str,
        remember_me: bool,
        request: Request,
        response: Response,
    ):
        db: Session = next(get_db())
        user = db.query(User).filter(User.email == email).first()

        if not user:
            raise LoginFailed("User not found.")

        if user and user.is_superuser != True:
            raise LoginFailed("User is not admin.")
        
        if not verify_password(password, user.hashed_password):
            raise LoginFailed("Invalid password.")
        
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        token_data = {
            "sub": user.email,
            "exp": datetime.now(timezone.utc) + access_token_expires,
        }
        access_token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)

        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            secure=True,
            samesite="lax",
        )

        return response


    async def is_authenticated(self, request: Request) -> Optional[User]:
        token = request.cookies.get("access_token")

        if not token:
            return None

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email: str = payload.get("sub")
            if email is None:
                return None

            db: Session = next(get_db())
            user = db.query(User).filter(User.email == email).first()

            if user is None or not user.is_superuser:
                return None

            return user

        except jwt.PyJWTError:
            return None

    async def logout(self, request: Request, response: Response) -> Response:
        response.delete_cookie("access_token")
        return response