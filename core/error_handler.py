from flask import jsonify


def base_error_handler(error):
    try:
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
    except:
        response = jsonify({"error": str(error), "code": 500})
        response.status_code = 500

    return response
