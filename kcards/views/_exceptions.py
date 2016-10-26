# pylint: disable=wildcard-import,unused-wildcard-import

from flask_api.exceptions import *


class Conflict(APIException):
    status_code = 409
    detail = "This resource already exists."
