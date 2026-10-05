from rest_framework.response import Response
from rest_framework.views import exception_handler


def api_exception_handler(exc, context):
    """Keep API errors stable and never serialize Python exception details."""
    response = exception_handler(exc, context)
    if response is None:
        return Response(
            {"code": "internal_error", "message": "The request could not be completed.", "errors": {}},
            status=500,
        )

    detail = response.data
    if isinstance(detail, dict) and "detail" in detail and len(detail) == 1:
        message = str(detail["detail"])
        errors = {}
    else:
        message = "The submitted information is invalid." if response.status_code == 400 else "The request could not be completed."
        errors = detail if isinstance(detail, dict) else {
            "non_field_errors": detail if isinstance(detail, list) else [str(detail)]
        }

    code_map = {
        400: "validation_error",
        401: "not_authenticated",
        403: "permission_denied",
        404: "not_found",
        405: "method_not_allowed",
        429: "rate_limited",
    }
    response.data = {"code": code_map.get(response.status_code, "request_error"), "message": message, "errors": errors}
    return response
