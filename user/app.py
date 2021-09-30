import json
import logging
from http import HTTPStatus

from connection import DBConnection
from encoder import DateTimeEncoder


def lambda_handler(event, _):
    logging.warning(f"Event successfully received: {event}")
    response, status = None, None

    method = event.get("httpMethod")
    params = event.get("queryStringParameters")
    body = event.get("body")

    if method == "GET" and params:
        response, status = get_user(params)

    elif body:
        logging.error(f"Missing body for {method} request")

        if method == "POST":
            response, status = post_user(body)

        elif method == "DELETE":
            response, status = delete_user(body)

        elif method == "PATCH":
            response, status = patch_user(body)

    else:
        response = {
            'message': 'Malformed request'
        }
        status = HTTPStatus.BAD_REQUEST

    return {
        "statusCode": status,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(response, cls=DateTimeEncoder)
    }


def get_user(params: dict):
    """
    Obtain the information of a single user. The parameters dictionary must only have
    the userId.
    :param params: Dictionary of query parameters.
    :return: The API response and status code.
    """
    required_params = ["userId"]

    if list(params.keys()) == required_params:
        db_conn = DBConnection()

        query = """
            SELECT     
                *
            FROM 
                cetac_user
            WHERE 
                id = %(user_id)s
        """

        params = {
            'user_id': params['userId'],
        }

        query_response, query_status_code = db_conn.execute_query(query, params)

        if query_status_code == HTTPStatus.OK:
            if query_response:
                response = {
                    'userData': query_response[0]
                }
                status = HTTPStatus.OK

            else:
                response = {
                    'message': "The user is not register on the DB."
                }
                status = HTTPStatus.NOT_FOUND

        else:
            response = {
                'message': "Error while obtaining the data"
            }
            status = HTTPStatus.INTERNAL_SERVER_ERROR

    else:
        response = {
            'message': "Missing query parameters"
        }
        status = HTTPStatus.BAD_REQUEST
        logging.error(params)

    return response, status


def post_user(params: dict):
    response = {
        'message': "Missing query parameters"
    }
    status = HTTPStatus.BAD_REQUEST

    

    return response, status


def delete_user(params: dict):
    response = {
        'message': "Missing query parameters"
    }
    status = HTTPStatus.BAD_REQUEST

    return response, status


def patch_user(params: dict):
    response = {
        'message': "Missing query parameters"
    }
    status = HTTPStatus.BAD_REQUEST

    return response, status
