from rest_framework.exceptions import APIException
from rest_framework import status


class CustomAPIException(APIException):
    error_key = "details"

    def as_dict(self):
        error_dict = super().as_dict()
        error_dict[self.error_key] = error_dict.pop("detail", None)
        return error_dict


class TypeErrorResponse(CustomAPIException):
    status_code = status.HTTP_417_EXPECTATION_FAILED
    default_detail = "Expected type error"
    default_code = "expected_type_error"

    def __init__(self, details=None):
        if details is not None:
            self.default_detail = details
        super().__init__()


class BadRequest(CustomAPIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Bad request"
    default_code = "bad_request"

    def __init__(self, details=None):
        if details is not None:
            self.default_detail = details
        super().__init__()


class UnAuthorizedError(CustomAPIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "Invalid credentials"
    default_code = "unauthorized"

    def __init__(self, details=None):
        if details is not None:
            self.default_detail = details
        super().__init__()


class ForbiddenError(CustomAPIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "This action is forbidden"
    default_code = "forbidden"

    def __init__(self, details=None):
        if details is not None:
            self.default_detail = details
        super().__init__()


class NotFoundError(CustomAPIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Item Not Found"
    default_code = "not_found"

    def __init__(self, details=None):
        if details is not None:
            self.default_detail = details
        super().__init__()


class ConflictError(CustomAPIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "Conflict"
    default_code = "conflict"

    def __init__(self, details=None):
        if details is not None:
            self.default_detail = details
        super().__init__()


class InternalServerError(CustomAPIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "Something went wrong"
    default_code = "internal_server_error"

    def __init__(self, details=None):
        if details is not None:
            self.default_detail = details
        super().__init__()


class ServiceUnavailable(CustomAPIException):
    status_code = status.HTTP_502_BAD_GATEWAY
    default_detail = "Bad Gateway"
    default_code = "bad_gateway"

    def __init__(self, details=None):
        if details is not None:
            self.default_detail = details
        super().__init__()


class ServiceUnavailable(CustomAPIException):
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    default_detail = "Service temporarily unavailable, try again later."
    default_code = "service_unavailable"

    def __init__(self, details=None):
        if details is not None:
            self.default_detail = details
        super().__init__()
