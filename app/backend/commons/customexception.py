from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException

from backend.utils.log import net_log, RESPONSE


def custom_exception_handler(exc, context):

    response = exception_handler(exc, context)

    if response is not None:
        try:
            print(response.data)
            custom_msg = response.data["custom_msg"]
        except:
            custom_msg = None
        response.data.clear()

        response.data["code"] = response.status_code

        if custom_msg is not None:
            response.data["msg"] = custom_msg
        elif response.status_code == 405:
            response.data["msg"] = "request not allowed"
        elif response.status_code == 401:
            response.data["msg"] = "authentication failed"
        elif response.status_code == 403:
            response.data["msg"] = "no access"
        elif response.status_code == 404:
            response.data["msg"] = "file not found"
        elif response.status_code >= 500:
            response.data["msg"] = "server exception"
        else:
            response.data["msg"] = "other unknown errors"

        response.data["data"] = None
        response.status_code = 200

    if response:
        net_log(response.data, RESPONSE)

    return response


class ParamsException(APIException):

    def __init__(self, error):
        self.detail = error
