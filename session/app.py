import json
import logging
from http import HTTPStatus

import cerberus

import session_schemas

from connection import DBConnection
from encoder import DateTimeEncoder


def lambda_handler(event, _):
    logging.warning(f"Event successfully received: {event}")
    response,status = None,None

    method = event.get("httpMethod")
    params = event.get("queryStringParameters")
    body = event.get("body")

    if method == "GET" and params:
        if "userId" in params.keys():
            response, status = get_session_listing(params)
        else:
            response, status = get_session(params)
    
    elif body:
        body = json.loads(body)

        if method == "POST":
            response, status = post_session(body)
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


def get_session(params: dict):
    required_params = ["sessionId"]
    if list(params.keys())==required_params:
        db_conn = DBConnection()
        query = """
            SELECT 
            tool,
            intervention_type,
            session_number,
            evaluation,
            session_date,
            motive,
            recovery_fee,
            record_id   
            FROM
            cetac_session
            WHERE
            id = %(session_id)s
        """
        params = {
            'session_id': params['sessionId'],
        }

        query_response, query_status_code = db_conn.execute_query(query, params)
    
        if query_status_code == HTTPStatus.OK:
            if query_response:
                response = {
                    'sessionData': query_response[0]
                    }
                status = HTTPStatus.OK

            else:
                response = {
                    'message': "The session is not register on the DB."
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


### TODO: FINISH LISTING
def get_session_listing(params):
    db_conn = DBConnection()

    required_params = "userId"

    if required_params in list(params.keys()):

        query = """
            SELECT
                cetac_session.id,
                session_date,
                intervention_type
            FROM
                (cetac_session
            INNER JOIN
                cetac_record
            ON
                cetac_session.record_id = cetac_record.id)
            WHERE
                cetac_record.user_id = %(userId)s
        """

        query_response, query_status_code = db_conn.execute_query(query, params)

        if query_status_code == HTTPStatus.OK:
            response = {
                'sessionList': query_response
            }
            status = HTTPStatus.OK

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


### PEDIR EL TIPO DE SESION Y HACER AJUSTE DE EKR Y HACER UPDATE DE RECORD
def post_session(body: dict):
    validator = cerberus.Validator(session_schemas.POST_SESSION_SCHEMA)

    if validator.validate(body):
        db_conn = DBConnection()

        _, query_status_code = db_conn.execute_query(
            query="""
            INSERT INTO cetac_session(
                tool,
                intervention_type,
                session_number,
                evaluation,
                session_date,
                motive,
                recovery_fee,
                record_id 
            ) Values(
                %(tool)s,
                %(intervention_type)s,
                %(session_number)s,
                %(evaluation)s,
                %(session_date)s,
                %(motive)s,
                %(recovery_fee)s,
                %(record_id)s
            )
            """,
            params=body
        )

        if query_status_code == HTTPStatus.OK:
            response = {
                'message': "Successfully added the session"
            }
            status = HTTPStatus.OK

        else:
            response = {
                'message': "Error while inserting the session"
            }
            status = HTTPStatus.INTERNAL_SERVER_ERROR

    else:
        response = {
            'message': "There was an error with the request",
            'error': validator.errors
        }
        status = HTTPStatus.BAD_REQUEST

    return response, status

