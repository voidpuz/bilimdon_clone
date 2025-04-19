from fastapi import Request, Response, HTTPException
from starlette_admin.auth import AdminConfig, AdminUser, AuthProvider
from starlette_admin.exceptions import FormValidationError, LoginFailed
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models import User
from app.utils import verify_password



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
        current_requested_user = db.query(User).filter(User.email == email).first()

        if not current_requested_user:
            raise LoginFailed("User not found.")

        if current_requested_user and current_requested_user.is_superuser != True:
            raise LoginFailed("User is not admin.")
        
        if not verify_password(password, current_requested_user.hashed_password):
            raise LoginFailed("Invalid password.")

        return response


    # async def is_authenticated(self, request) -> bool:
    #     auth_header = request.headers.get("Authorization")
    #     is_bearer = auth_header.startswith("Bearer ") if auth_header else False
    #     token = auth_header.split(" ")[1] if auth_header else ""

    #     if not auth_header and is_bearer:
    #         raise HTTPException(
    #             status_code=401,
    #             detail="You are not authenticated."
    #         )


    #     try:
    #         decoded_jwt = jwt.decode(
    #             token,
    #             SECRET_KEY,
    #             ALGORITHM
    #         )
    #         print(decoded_jwt)
    #         email = decoded_jwt.get("email")
    #         password = decoded_jwt.get("password")

    #         db_user = db.query(User).filter(User.email == email).first()

    #     except:
    #         raise HTTPException(
    #             status_code=401,
    #             detail="Invalid token."
    #         )

    #     return db_user