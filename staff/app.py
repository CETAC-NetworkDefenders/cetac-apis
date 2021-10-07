import json
import logging
from http import HTTPStatus

import cerberus

import staff_schemas
from connection import DBConnection
from encoder import DateTimeEncoder
from staff_queries import StaffQueries


def lambda_handler(event, _):
    logging.warning(f"Event successfully received: {event}")
    response, status = None, None

    method = event.get("httpMethod")
    params = event.get("queryStringParameters")
    body = event.get("body")

    if method == "GET" and params:
        if "listing" in params.keys():
            response, status = get_staff_listing(params)

        else:
            response, status = get_staff(params)

    elif body:
        body = json.loads(body)

        if method == "POST":
            response, status = post_staff(body)

        elif method == "DELETE":
            response, status = delete_staff(body)

        elif method == "PATCH":
            response, status = patch_staff(body)

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


def get_staff(params: dict):
    """
    Obtain the information of a single staff. The parameters dictionary must only have
    the staffId.
    :param params: Dictionary of query parameters.
    :return: The API response and status code.
    """
    validator = cerberus.Validator(staff_schemas.GET_DELETE_STAFF_SCHEMA)

    if validator.validate(params):
        db_conn = DBConnection()
        query_params = {
            'staff_id': params['staffId'],
        }

        query_response, query_status_code = db_conn.execute_query(
            query=StaffQueries.get_staff_info.value,
            params=query_params
        )

        if query_status_code == HTTPStatus.OK:
            if query_response:
                response = {
                    'staffData': query_response[0]
                }
                status = HTTPStatus.OK

            else:
                response = {
                    'message': "The staff is not register on the DB."
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


def get_staff_listing(params: dict):
    """
    Obtain a list with the lastnames and name of every registered staff.
    :param params: Dictionary with query parameters. In this case, there must be listing,
    whose value does not matter since this is just a flag, and accessLevel, which indicates the
    first filter on the staff table.
    :return:
    """
    validator = cerberus.Validator(staff_schemas.GET_STAFF_LISTING_SCHEMA)

    if validator.validate(params):
        db_conn = DBConnection()

        query = StaffQueries.get_staff_listing.value
        query_params = {
            'access_level': params['accessLevel']
        }

        lastname_filter = params.get("lastnameFilter")
        if lastname_filter:
            query += StaffQueries.listing_filter.value
            query_params['first_lastname']: lastname_filter

        elif params['accessLevel'] == 'admin':
            query += StaffQueries.two_filters.value
            query_params['access_level2'] = 'admin_support'

        query_response, query_status_code = db_conn.execute_query(query=query, params=query_params)

        if query_status_code == HTTPStatus.OK:
            response = {
                'staffList': query_response
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


def post_staff(body: dict):
    """
    Add a new staff to the DB
    :param body
    :return:
    """
    validator = cerberus.Validator(staff_schemas.POST_STAFF_SCHEMA)

    if validator.validate(body):
        db_conn = DBConnection()

        _, query_status_code = db_conn.execute_query(
            query=StaffQueries.create_staff.value,
            params=body
        )

        if query_status_code == HTTPStatus.OK:
            response = {
                'message': "Successfully added the staff"
            }
            status = HTTPStatus.OK

        else:
            response = {
                'message': "Error while inserting the staff"
            }
            status = HTTPStatus.INTERNAL_SERVER_ERROR

    else:
        response = {
            'message': "There was an error with the request",
            'error': validator.errors
        }
        status = HTTPStatus.BAD_REQUEST

    return response, status


def delete_staff(params: dict):
    """
    Delete a staff from the DB
    :param params:
    :return:
    """
    validator = cerberus.Validator(staff_schemas.GET_DELETE_STAFF_SCHEMA)

    if validator.validate(params):
        db_conn = DBConnection()
        query_params = {
            'staff_id': params['staffId'],
        }

        _, query_status_code = db_conn.execute_query(
            query=StaffQueries.delete_staff.value,
            params=query_params
        )

        if query_status_code == HTTPStatus.OK:
            response = {
                'message': "Successfully deleted the staff"
            }
            status = HTTPStatus.OK

        else:
            response = {
                'message': "Error while deleting the staff"
            }
            status = HTTPStatus.INTERNAL_SERVER_ERROR

    else:
        response = {
            'message': "There was an error with the request",
            'error': validator.errors
        }
        status = HTTPStatus.BAD_REQUEST
    return response, status


def patch_staff(params: dict):
    """
    Update a staff member to the DB
    :param body
    :return:
    """
    validator = cerberus.Validator(staff_schemas.PATCH_STAFF_SCHEMA)

    if validator.validate(params):
        db_conn = DBConnection()

        _, query_status_code = db_conn.execute_query(
            query = StaffQueries.update_staff.value, params=params
        )

        if query_status_code == HTTPStatus.OK:
            response = {
                'message': "Succesfully updated the user"
            }
            status=HTTPStatus.OK

        else:
            response = {
                'message': "Error while updating the usre"
            }
            status = HTTPStatus.INTERNAL_SERVER_ERROR



    else:
        response = {
            'message': "There was an error with the request",
            'error': validator.errors
        }
        status = HTTPStatus.BAD_REQUEST

    return response, status

