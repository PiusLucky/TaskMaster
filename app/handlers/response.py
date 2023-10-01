
from flask import jsonify


def success_response(data=None, message="Success", status_code=200):
    result = {
        "meta": {
            "statusCode": status_code,
            "message": message,
        },
        "data": data  # Don't jsonify here
    }
    response = jsonify(result)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response, status_code  # Return the JSON response


def error_response(message="An error occurred", status_code=500):
    result = {
        "meta": {
            "statusCode": status_code,
            "message": message,
        }
    }

    response = jsonify(result)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response, status_code
