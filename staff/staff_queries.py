from enum import Enum


class StaffQueries(Enum):

	get_staff_info = """
		SELECT
			id,     
			first_lastname,
			second_lastname, 
			firstname, 
			email, 
			access_level, 
			cellphone, 
			zip_code, 
			street, 
			neighborhood, 
			address_number
		FROM 
			cetac_staff
		WHERE 
			id = %(staff_id)s
	"""

	get_staff_listing = """
		SELECT
			id,
			first_lastname,
			second_lastname,
			firstname
		FROM 
			cetac_staff
		WHERE 
			access_level = %(access_level)s
	"""

	create_staff = """
		INSERT INTO cetac_staff (
			first_lastname,
			second_lastname, 
			firstname, 
			access_level, 
			cellphone, 
			zip_code, 
			street, 
			neighborhood, 
			address_number, 
			email,
			password,
			salt
		) VALUES (
			%(first_lastname)s, 
			%(second_lastname)s, 
			%(firstname)s, 
			%(access_level)s, 
			%(cellphone)s, 
			%(zip_code)s, 
			%(street)s, 
			%(neighborhood)s, 
			%(address_number)s, 
			%(username)s, 
			%(password)s, 
			%(salt)s			
		);
	"""

	update_staff = """
		UPDATE 
			cetac_staff
		SET 
			first_lastname = %(first_lastname)s,
			second_lastname = %(second_lastname)s, 
			firstname = %(firstname)s, 
			cellphone = %(cellphone)s, 
			zip_code = %(zip_code)s, 
			street = %(street)s, 
			neighborhood = %(neighborhood)s, 
			address_number = %(address_number)s
		WHERE 
			id = %(id)s
	"""

	delete_staff = """
		DELETE FROM 
			cetac_staff
		WHERE
			id = %(staff_id)s
	"""

	get_intervention_type_report = """
		SELECT
			intervention_type AS name,
			COUNT(intervention_type) AS val
		FROM
			cetac_session
		WHERE
			session_date <= CURRENT_DATE AND 
			session_date >= %(timespan)s
		GROUP BY
			intervention_type
	"""

	get_service_type_report = """
		SELECT
			service_type AS name,
			COUNT(service_type) AS val
		FROM
			cetac_session
		WHERE
			session_date <= CURRENT_DATE AND 
			session_date >= %(timespan)s
		GROUP BY
			service_type
	"""

	get_motive_report = """
		SELECT
			motive AS name,
			COUNT(motive) AS val
		FROM
			cetac_session
		WHERE
			session_date <= CURRENT_DATE AND 
			session_date >= %(timespan)s
		GROUP BY
			motive
	"""


	get_users_report = """
		SELECT
			gender,
			count(gender) AS total
		FROM 
			(
				SELECT DISTINCT
					user_id
				FROM 
					cetac_session
				JOIN
					cetac_record
				ON
					cetac_session.record_id = cetac_record.id
				WHERE
					session_date >= date_trunc(%(timeframe)s, CURRENT_DATE)
			) AS user_id
		JOIN
			cetac_user
		ON
			user_id = cetac_user.id
		GROUP BY
			gender
		"""

	get_users_report_by_thanatologist = """
		SELECT 
			concat(firstname, ' ', first_lastname, ' ', second_lastname) AS thanatologist,
			count(staff_id) AS total
		FROM 
			cetac_session
		JOIN 
			cetac_staff
		ON
			cetac_staff.id = cetac_session.staff_id
		WHERE
			session_date >= date_trunc(%(timeframe)s, CURRENT_DATE)
		AND
			staff_id is not null
		GROUP BY
			staff_id, firstname, first_lastname, second_lastname
	"""

	get_recovery_fees_report = """
		SELECT
			SUM (recovery_fee) AS total
		FROM
			cetac_session
		WHERE
			session_date >= date_trunc(%(timeframe)s, CURRENT_DATE)
	"""

	get_recovery_fees_report_by_thanatologist = """
		SELECT
			concat(firstname, ' ', first_lastname, ' ', second_lastname) AS thanatologist,
			SUM (recovery_fee) AS total
		FROM
			cetac_session
		JOIN
			cetac_staff
		ON
			cetac_staff.id = cetac_session.staff_id
		WHERE
			session_date >= date_trunc(%(timeframe)s, CURRENT_DATE)
		AND
			staff_id is not null
		GROUP BY
			staff_id, firstname, first_lastname, second_lastname
	"""
