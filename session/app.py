import json
import logging
from http import HTTPStatus

from connection import DBConnection
from encoder import DateTimeEncoder


def lambda_handler(event, _):
    logging.warning(f"Event successfully received: {event}")

    db_conn = DBConnection()

    query = "SELECT * FROM cetac_user"
    query_response = db_conn.execute_query(query)

    response = {
        'queryResponse': query_response
    }

    return {
        "statusCode": HTTPStatus.OK,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(response, cls=DateTimeEncoder)
    }
