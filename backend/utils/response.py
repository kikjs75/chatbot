import json


def api_response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        },
        "body": json.dumps(body, ensure_ascii=False),
    }


def success(data):
    return api_response(200, data)


def bad_request(message="Bad Request"):
    return api_response(400, {"error": message})


def not_found(message="Not Found"):
    return api_response(404, {"error": message})


def server_error(message="Internal Server Error"):
    return api_response(500, {"error": message})
