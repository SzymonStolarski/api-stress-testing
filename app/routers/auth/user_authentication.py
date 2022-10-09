from passlib.context import CryptContext

from entities.user import UserInDB


class UserAuthenticator:
    password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @staticmethod
    def authenticate_user(db, username: str, password: str):
        user = UserAuthenticator.__get_user(db, username)

        if not user:
            return False
        if not UserAuthenticator.__verify_password(password,
                                                   user.hashed_password):
            return False

        return user

    def __verify_password(plain_password: str,
                          hashed_password: str) -> bool:
        return UserAuthenticator.password_context.verify(
            plain_password, hashed_password)

    def __get_user(db, username: str):
        if username in db:
            user_dict = db[username]

            return UserInDB(**user_dict)
