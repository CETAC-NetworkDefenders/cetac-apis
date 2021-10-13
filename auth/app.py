import json
import logging
from http import HTTPStatus

from connection import DBConnection
from encoder import DateTimeEncoder


def lambda_handler(event, _):
	logging.warning(f"Event successfully received: {event}")

	method = event.get("httpMethod")
	params = event.get("queryStringParameters")

	if method == "GET" and params:
		if "password" in params.keys():
			response, status = auth_user(params)

		else:
			response, status = get_salt(params)

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


def get_salt(params):
	"""
	Obtain the salt of a user given the username. This must be obtained beforehand so that the
	password is not sent only over HTTPS encryption.
	:param params:
	:return:
	"""
	db_conn = DBConnection()
	query = """
		SELECT 
			id,
			salt
		FROM 
			cetac_staff
		WHERE 
			username = %(username)s
	"""
	query_result, status_code = db_conn.execute_query(query=query, params=params)

	if status_code == HTTPStatus.OK and query_result:
		response = query_result[0]
		status_code = HTTPStatus.OK

	else:
		response = {
			"id": None,
			"salt": None
		}
		status_code = HTTPStatus.NOT_FOUND

	return response, status_code


def auth_user(params):
	input_password = params.pop("password")

	db_conn = DBConnection()
	query = """
		SELECT 
			access_level, 
			password, 
			firstname
		FROM 
			cetac_staff
		WHERE 
			id = %(id)s
	"""
	query_result, status_code = db_conn.execute_query(query=query, params=params)

	if status_code == HTTPStatus.OK and query_result:
		password = query_result[0].pop("password")

		if password == input_password:
			status_code = HTTPStatus.OK
			response = query_result[0]

		else:
			response = {
				"firstname": None,
				"access_level": None
			}
			status_code = HTTPStatus.FORBIDDEN

	else:
		response = {
			"firstname": None,
			"access_level": None
		}
		status_code = HTTPStatus.NOT_FOUND

	return response, status_code
