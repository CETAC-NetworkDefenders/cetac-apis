import base64
import boto3
import json
import logging
import os
from botocore.exceptions import ClientError
from http import HTTPStatus

import psycopg2
import psycopg2.extras


class DBConnection:
	"""
	This class abstracts a DB connection so that only the query is defined and the execution is
	done out of the box.
	"""
	def __init__(self):
		self.db_name = os.environ["DB_NAME"]
		self.db_secret_name = os.environ["DB_SECRET_NAME"]
		self.db_secret_region = os.environ["DB_SECRET_REGION"]
		self.db_data = self.get_db_credentials()
		self.conn = self.create_db_connection()

	def get_db_credentials(self) -> dict:
		"""
		Obtains the DB access information from an AWS Secret. First creates a connection to the
		service and then gets the specific value.
		:return: A dictionary of the DB Secrets.
		"""
		session = boto3.session.Session()
		client = session.client(
			service_name='secretsmanager',
			region_name=self.db_secret_region
		)

		try:
			secret_response = client.get_secret_value(SecretId=self.db_secret_name)

		except ClientError as exc:
			logging.error(f"Error while retrieving the DB Credentials Secret: {exc.response}")
			secrets = None

		else:
			if 'SecretString' in secret_response:
				secrets = json.loads(secret_response['SecretString'])
			else:
				secrets = json.loads(base64.b64decode(secret_response['SecretBinary']))

		return secrets

	def create_db_connection(self):
		"""
		Creates a connection to the DB using the access data obtained from the Secret.
		:return:
		"""
		try:
			conn = psycopg2.connect(
				host=self.db_data['host'],
				port=self.db_data['port'],
				database=self.db_name,
				user=self.db_data['username'],
				password=self.db_data['password']
			)

		except psycopg2.OperationalError as error:
			logging.error(f"Not possible to connect to the DB. Error: {str(error)}")
			conn = None

		return conn

	def execute_query(self, query: str, params: dict = None) -> dict:
		"""
		Executes a query. If the query is a SELECT statement, it returns all the result rows in
		the form of a list of dictionaries. Otherwise, it only returns the status code indicating if
		the query was successful.
		:return: A dictionary with the statusCode of the query in every case. If the query was a
		SELECT statement, return also the queryResponse as a list of dictionaries.
		"""
		if not self.conn:
			self.conn = self.create_db_connection()

		is_select_statement = query.strip().startswith("SELECT")

		if not is_select_statement and not params:
			query_response = {
				'statusCode': HTTPStatus.BAD_REQUEST,
				'message': "Should use query parameters when performing queries with side effects."
			}

		else:
			query_cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

			try:
				query_cursor.execute(query=query, vars=params)

			except (psycopg2.OperationalError, psycopg2.DatabaseError) as exc:
				logging.error(f"Error while executing the query. Query: {query}. Error: {str(exc)}")
				query_response = {'statusCode': HTTPStatus.INTERNAL_SERVER_ERROR}

			else:
				query_response = {'statusCode': HTTPStatus.OK}

				if is_select_statement:
					query_response['queryResult'] = query_cursor.fetchall()

				else:
					query_cursor.commit()

				query_cursor.close()

		return query_response
