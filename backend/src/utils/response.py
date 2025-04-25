from flask import jsonify


def create_response(is_success=True, data=None, message=None, http_status=200):
    """
    Create an API response with simplified success/error format.

    Args:
        is_success (bool): Whether the operation was successful
        data: Payload for successful responses
        message: Error message for failed responses
        http_status: HTTP status code
    """

    if is_success:
        response = {"status": "success", "data": data}
    else:
        response = {"status": "error", "message": message}
    return jsonify(response), http_status
