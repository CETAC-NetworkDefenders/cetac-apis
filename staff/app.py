import json
import logging
from http import HTTPStatus
from datetime import timedelta, date

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

    logging.warning("Continue with event execution")
    logging.warning(f"Received body {body}")

    if method == "GET" and params:
        if "listing" in params.keys():
            logging.warning("Listing staff")
            response, status = get_staff_listing(params)

        elif "session_report" in params.keys():
            logging.warning("Getting session type report")
            response, status = get_session_report(params)

        elif "users_report" in params.keys():
            logging.warning("Getting staff users report")
            response, status = get_users_report(params)

        elif "users_report_by_thanatologist" in params.keys():
            logging.warning("Getting staff users report by thanatologist")
            response, status = get_users_report_by_thanatologist(params)

        elif "recovery_fees_report" in params.keys():
            logging.warning("Getting staff recovery fees report")
            response, status = get_recovery_fees_report(params)

        elif "recovery_fees_report_by_thanatologist" in params.keys():
            logging.warning("Getting staff recovery fees report by thanatologist")
            response, status = get_recovery_fees_report_by_thanatologist(params)

        else:
            response, status = get_staff(params)

    elif body:
        logging.warning(type(body))
        body = json.loads(body)
        logging.warning(f"Body after loading {body}")

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

        query_response, query_status_code = db_conn.execute_query(
            query=StaffQueries.get_staff_info.value,
            params=params
        )

        if query_status_code == HTTPStatus.OK:
            if query_response:
                response = query_response[0]
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
        query_response, query_status_code = db_conn.execute_query(query=query, params=params)

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

        _, query_status_code = db_conn.execute_query(
            query=StaffQueries.delete_staff.value,
            params=params
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
    logging.warning("Executing patch")

    if validator.validate(params):
        logging.warning("Passed validation")
        db_conn = DBConnection()

        _, query_status_code = db_conn.execute_query(
            query=StaffQueries.update_staff.value, params=params
        )

        if query_status_code == HTTPStatus.OK:
            logging.warning("Successfully updated the user")
            response = {
                'message': "Succesfully updated the user"
            }
            status=HTTPStatus.OK

        else:
            logging.warning("Error while updating the user")
            response = {
                'message': "Error while updating the user"
            }
            status = HTTPStatus.INTERNAL_SERVER_ERROR
    else:
        logging.warning(f"Does not pass validation {validator.errors}")
        response = {
            'message': "There was an error with the request",
            'error': validator.errors
        }
        status = HTTPStatus.BAD_REQUEST

    return response, status


def get_session_report(params: dict):
        validator = cerberus.Validator(staff_schemas.GET_INTERVENTION_TYPE_REPORT_SCHEMA)

        if validator.validate(params):

            query_mapping = {
                'intervention': StaffQueries.get_intervention_type_report.value,
                'service': StaffQueries.get_service_type_report.value,
                'motive': StaffQueries.get_motive_report.value
            }

            timediff_maping = {
                'week': timedelta(weeks=1),
                'month': timedelta(weeks=4),
                'year': timedelta(weeks=52)
            }
            key_mapping = {
                'Herramientas Alternativas': "Alternativas",
                'Servicios Holisticos': "Holísticos",
                'Servicios Acompañamiento': "Acompañamiento"
            }
            basetime = date.today() - timediff_maping[params['timespan']]

            logging.warning(query_mapping[params['session_report']])
            logging.warning(f"Basetime: {basetime.strftime('%Y-%m-%d')}")

            db_conn = DBConnection()

            query_response, query_status_code = db_conn.execute_query(
                query=query_mapping[params['session_report']],
                params={'timespan': basetime.strftime('%Y-%m-%d')}
            )

            if query_status_code == HTTPStatus.OK:
                logging.warning(f"Raw query result: {query_response}")
                names = []
                values = []

                for row in query_response:
                    names.append(key_mapping.get(row['name'], row['name']))
                    values.append(row['val'])

                response = {
                    'labels': names,
                    'values': values
                }
                status = HTTPStatus.OK
                logging.warning(f"Processed response: {response}")

            else:
                logging.error("Error in the DB")
                response = {
                    'message': "Error while obtaining the data"
                }
                status = HTTPStatus.INTERNAL_SERVER_ERROR

        else:
            logging.error(f"Validator Error {validator.errors}")
            response = {
                'message': "There was an error with the request",
                'error': validator.errors
            }
            status = HTTPStatus.BAD_REQUEST

        return response, status


def get_users_report(params: dict):
    """
    """
    validator = cerberus.Validator(staff_schemas.GET_USERS_REPORT_SCHEMA)

    if validator.validate(params):
        db_conn = DBConnection()

        query_response, query_status_code = db_conn.execute_query(
            query=StaffQueries.get_users_report.value,
            params=params
        )

        if query_status_code == HTTPStatus.OK:
            response = {
                'report': query_response
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


def get_users_report_by_thanatologist(params: dict):
    """
    """
    validator = cerberus.Validator(staff_schemas.GET_USERS_REPORT_BY_THANATOLOGIST_SCHEMA)

    if validator.validate(params):
        db_conn = DBConnection()

        query_response, query_status_code = db_conn.execute_query(
            query=StaffQueries.get_users_report_by_thanatologist.value,
            params=params
        )

        if query_status_code == HTTPStatus.OK:
            response = {
                'report': query_response
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


def get_recovery_fees_report(params: dict):
    """
    """
    validator = cerberus.Validator(staff_schemas.GET_RECOVERY_FEES_REPORT_SCHEMA)

    if validator.validate(params):
        db_conn = DBConnection()

        query_response, query_status_code = db_conn.execute_query(
            query=StaffQueries.get_recovery_fees_report.value,
            params=params
        )

        if query_status_code == HTTPStatus.OK:
            response = {
                'report': query_response
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


def get_recovery_fees_report_by_thanatologist(params: dict):
    """
    """
    validator = cerberus.Validator(staff_schemas.GET_RECOVERY_FEES_REPORT_BY_THANATOLOGIST_SCHEMA)

    if validator.validate(params):
        db_conn = DBConnection()

        query_response, query_status_code = db_conn.execute_query(
            query=StaffQueries.get_recovery_fees_report_by_thanatologist.value,
            params=params
        )

        if query_status_code == HTTPStatus.OK:
            response = {
                'report': query_response
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


### TODO: PUT RECIBE USER ID, reabre el expediente y lo asigna al nuevo staff

