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
    if list(params.keys()) == required_params:
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
                record_id, 
                service_type
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
                response = query_response[0]
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


def post_session(body: dict):
    validator = cerberus.Validator(session_schemas.POST_SESSION_SCHEMA)
    validator.allow_unknown = True

    logging.warning("Received a POST request")

    if validator.validate(body):
        logging.warning("Passed validation")
        db_conn = DBConnection()

        query = """
            WITH past as (
                SELECT 
                    session_number 
                FROM 
                    cetac_session
                WHERE 
                    record_id = %(record_id)s
                ORDER BY 
                    session_date DESC 
                LIMIT 1
            ) INSERT INTO cetac_session(
                tool,
                intervention_type,
                session_number,
                evaluation,
                session_date,
                motive,
                recovery_fee,
                record_id, 
                service_type
            ) VALUES (
                %(tool)s,
                %(intervention_type)s,
                (CASE
                    WHEN EXISTS(SELECT session_number FROM past)
                    THEN (SELECT session_number+1 FROM past)
                    ELSE 1
                END), 
                %(evaluation)s,
                %(session_date)s,
                %(motive)s,
                %(recovery_fee)s,
                %(record_id)s, 
                %(service_type)s
            ); 
            UPDATE 
                cetac_record 
            SET 
                is_open = %(is_open)s
            WHERE
                id = %(record_id)s
        """

        _, query_status_code = db_conn.execute_query(query, body)

        if query_status_code == HTTPStatus.OK:
            logging.warning("Executed query succesfully")

            response = {
                'message': "Successfully added the session"
            }
            status = HTTPStatus.OK

        else:
            logging.error("Error in the query")
            response = {
                'message': "Error while inserting the session"
            }
            status = HTTPStatus.INTERNAL_SERVER_ERROR

    else:
        logging.error(f"Validation error {validator.errors}")
        response = {
            'message': "There was an error with the request",
            'error': validator.errors
        }
        status = HTTPStatus.BAD_REQUEST

    return response, status

