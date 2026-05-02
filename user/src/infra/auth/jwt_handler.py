import jwt
from src.infra.exceptions.exceptions import InvalidTokenException

class JWTHandler:
    
    def is_token_valid(
        self,
        token: str,
    ) -> str:
        try:
            jwt.decode(
                token,
                options={
                    "verify_signature": False,
                    "verify_exp": True,
                },
            )
            return token
        except jwt.exceptions.PyJWTError as ex:
            raise InvalidTokenException(status_code=401, message=str(ex))
    