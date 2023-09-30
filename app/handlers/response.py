
from flask import jsonify

# Custom success response handler
def success_response(data=None, message="Success", status_code=200):
    result = {
        "meta": {
            "statusCode": status_code,
            "message": message,
        },
        "data": data  # Don't jsonify here
    }

    return jsonify(result), status_code  # Return the JSON response

# Custom error response handler
def error_response(message="An error occurred", status_code=500):
    result = {
        "meta": {
            "statusCode": status_code,
            "message": message,
        }
    }

    return result, status_code