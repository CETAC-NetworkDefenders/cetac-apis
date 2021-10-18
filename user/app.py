import json
import logging
from http import HTTPStatus

import cerberus

import user_schemas
from connection import DBConnection
from encoder import DateTimeEncoder
from user_queries import UserQueries


def lambda_handler(event, _):
    logging.warning(f"Event successfully received: {event}")
    response, status = None, None

    method = event.get("httpMethod")
    params = event.get("queryStringParameters")
    body = event.get("body")

    if method == "GET" and params:
        if "staffId" in params.keys():
            response, status = get_user_listing_by_staff_id(params)
        elif "listing" in params.keys():
            response, status = get_user_listing(params)
        else:
            response, status = get_user(params)

    elif body:
        body = json.loads(body)
        logging.warning(f"Loaded JSON: {body}")

        if method == "POST":
            response, status = post_user(body, params)

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
    validator = cerberus.Validator(user_schemas.GET_USER_SCHEMA)

    if validator.validate(params):
        db_conn = DBConnection()
        query_params = {
            'user_id': params['userId'],
        }

        query_response, query_status_code = db_conn.execute_query(
            query = UserQueries.get_user.value,
            params = query_params)

        if query_status_code == HTTPStatus.OK:
            if query_response:
                response = query_response[0]
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
            'message': "There was an error with the request",
            'error': validator.errors
        }
        status = HTTPStatus.BAD_REQUEST
        logging.error(params)

    return response, status


def get_user_listing(params: dict):
    """
    Obtain a list with the lastnames and name of every registered user.
    :param params: Dictionary with query parameters.
    :return:
    """
    validator = cerberus.Validator(user_schemas.GET_USER_LISTING_SCHEMA)

    if validator.validate(params):
        db_conn = DBConnection()

        query = UserQueries.get_user_listing.value
        query_params = {
            'listing': params['listing']
        }

        query_response, query_status_code = db_conn.execute_query(query=query, params=query_params)

        if query_status_code == HTTPStatus.OK:
            response = {
                'userList': query_response
            }
            status = HTTPStatus.OK

        else:
            response = {
                'message': "Error while obtaining the data"
            }
            status = HTTPStatus.INTERNAL_SERVER_ERROR

    else:
        response = {
            'message': "There was an error with the request",
            'error': validator.errors
        }
        status = HTTPStatus.BAD_REQUEST

    return response, status


def get_user_listing_by_staff_id(params: dict):
    """
    Obtain a list with the lastnames and name of all users attended by thanatologist.
    :param params: Dictionary with query parameters.
    :return:
    """
    validator = cerberus.Validator(user_schemas.GET_USER_LISTING_BY_STAFF_ID_SCHEMA)

    if validator.validate(params):
        db_conn = DBConnection()

        query = UserQueries.get_user_listing_by_staff_id.value
        query_params = {
            'listing': params['listing'],
            'staff_id': params['staffId']
        }

        query_response, query_status_code = db_conn.execute_query(query=query, params=query_params)

        if query_status_code == HTTPStatus.OK:
            response = {
                'userList': query_response
            }
            status = HTTPStatus.OK

        else:
            response = {
                'message': "Error while obtaining the data"
            }
            status = HTTPStatus.INTERNAL_SERVER_ERROR

    else:
        response = {
            'message': "There was an error with the request",
            'error': validator.errors
        }
        status = HTTPStatus.BAD_REQUEST

    return response, status


def post_user(body: dict, params:dict):
    """
    Add a new user to the DB
    :param body
    :param params
    :return:
    """
    validator = cerberus.Validator(user_schemas.POST_USER_SCHEMA)
    validator.allow_unknown = True

    if validator.validate(body) and 'staff_id' in params:
        db_conn = DBConnection()

        body['staff_id'] = params['staff_id']

        _, query_status_code = db_conn.execute_query(
            query=UserQueries.create_user.value,
            params=body
        )

        if query_status_code == HTTPStatus.OK:
            response = {
                'message': "Successfully added the user"
            }
            status = HTTPStatus.OK

        else:
            response = {
                'message': "Error while inserting the user"
            }
            status = HTTPStatus.INTERNAL_SERVER_ERROR

    else:
        response = {
            'message': "There was an error with the request",
            'error': validator.errors
        }
        status = HTTPStatus.BAD_REQUEST

    return response, status


def patch_user(body: dict):
    """
    Add a new user to the DB
    :param body
    :return:
    """
    validator = cerberus.Validator(user_schemas.PATCH_USER_SCHEMA)
    validator.allow_unknown = True

    if validator.validate(body):
        logging.warning(f"Validation pass")
        db_conn = DBConnection()

        _, query_status_code = db_conn.execute_query(
            query=UserQueries.update_user.value,
            params=body
        )

        if query_status_code == HTTPStatus.OK:
            logging.warning(f"Query executed")
            response = {
                'message': "Successfully updated the user"
            }
            status = HTTPStatus.OK

        else:
            logging.error(f"Error while updating the user")
            response = {
                'message': "Error while updating the user"
            }
            status = HTTPStatus.INTERNAL_SERVER_ERROR

    else:
        response = {
            'message': "There was an error with the request",
            'error': validator.errors
        }
        logging.error(validator.errors)
        status = HTTPStatus.BAD_REQUEST

    return response, status

