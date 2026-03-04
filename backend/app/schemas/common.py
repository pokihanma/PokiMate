from typing import Any, Generic, TypeVar

T = TypeVar("T")


class SuccessResponse(Generic[T]):
    success: bool = True
    data: T


class ErrorResponse:
    success: bool = False
    error: str
