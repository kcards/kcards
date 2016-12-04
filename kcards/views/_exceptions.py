# pylint: disable=wildcard-import,unused-wildcard-import

from flask_api.exceptions import *


class Conflict(APIException):
    status_code = 409
    detail = "This resource already exists."


class UnprocessableEntity(APIException):
    status_code = 422
    detail = "Unable to process the request."
