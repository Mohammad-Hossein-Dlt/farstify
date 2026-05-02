from typing import Any
from pydantic import BaseModel


class DefaultModel(BaseModel):
    detail: str

class ResponseMessage:
    @staticmethod
    def HTTP_200_OK(description: str, model = DefaultModel) -> dict:
        return {200: {"model": model, "description": description}}

    @staticmethod
    def HTTP_201_CREATED(description: str, model = DefaultModel) -> dict:
        return {201: {"model": model, "description": description}}

    @staticmethod
    def HTTP_202_ACCEPTED(description: str, model = DefaultModel) -> dict:
        return {202: {"model": model, "description": description}}

    @staticmethod
    def HTTP_203_NON_AUTHORITATIVE_INFORMATION(description: str, model = DefaultModel) -> dict:
        return {203: {"model": model, "description": description}}

    @staticmethod
    def HTTP_204_NO_CONTENT(description: str, headers: dict[str, Any]) -> dict:
        return {204: {"description": description, "headers": headers}}

    @staticmethod
    def HTTP_400_BAD_REQUEST(description: str, model = DefaultModel) -> dict:
        return {400: {"model": model, "description": description}}

    @staticmethod
    def HTTP_401_UNAUTHORIZED(description: str, model = DefaultModel) -> dict:
        return {401: {"model": model, "description": description}}

    @staticmethod
    def HTTP_402_PAYMENT_REQUIRED(description: str, model = DefaultModel) -> dict:
        return {402: {"model": model, "description": description}}

    @staticmethod
    def HTTP_403_FORBIDDEN(description: str, model = DefaultModel) -> dict:
        return {403: {"model": model, "description": description}}

    @staticmethod
    def HTTP_404_NOT_FOUND(description: str, model = DefaultModel) -> dict:
        return {404: {"model": model, "description": description}}

    @staticmethod
    def HTTP_405_METHOD_NOT_ALLOWED(description: str, model = DefaultModel) -> dict:
        return {405: {"model": model, "description": description}}

    @staticmethod
    def HTTP_409_CONFLICT(description: str, model = DefaultModel) -> dict:
        return {409: {"model": model, "description": description}}

    @staticmethod
    def HTTP_429_TOO_MANY_REQUESTS(description: str, model = DefaultModel) -> dict:
        return {429: {"model": model, "description": description}}

    @staticmethod
    def HTTP_422_UNPROCESSABLE_ENTITY(description: str, model = DefaultModel) -> dict:
        return {422: {"model": model, "description": description}}

    @staticmethod
    def HTTP_498_INVALID_TOKEN(description: str, model = DefaultModel) -> dict:
        return {498: {"model": model, "description": description}}

    @staticmethod
    def HTTP_500_INTERNAL_SERVER_ERROR(description: str, model = DefaultModel) -> dict:
        return {500: {"model": model, "description": description}}
