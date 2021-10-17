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
			intervention_type,
			COUNT(intervention_type) AS total
		FROM
			cetac_session
		GROUP BY
			intervention_type
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
	