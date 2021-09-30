import json
import logging
from http import HTTPStatus

from connection import DBConnection
from encoder import DateTimeEncoder


def lambda_handler(event, _):
    logging.warning(f"Event successfully received: {event}")
    response,status = None,None

    method = event.get("httpMethod")
    params = event.get("queryStringParameters")
    body = event.get("body")

    if method == "GET" and params:
        response, status = get_session(params)
    elif body:
        logging.error(f"Missing body for {method} request")

        if mehod == "POST":
            response,status = post_session(body)
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
                session_date,
                session_number,
                motive,
                intervention_type,
                tool,
                record_id,
                recovery_fee
                FROM
                    cetac_session
                WHERE
                    id = %(session_id)s
                    """
        params = {
            'session_id': params['sessionId'],
        }

    query_response = db_conn.execute_query(query, params)
    
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

   

    
