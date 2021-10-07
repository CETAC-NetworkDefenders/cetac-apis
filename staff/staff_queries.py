from enum import Enum


class StaffQueries(Enum):

	get_staff_info = """
		SELECT     
			first_lastname,
			second_lastname, 
			firstname, 
			username, 
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
			username,
			password,
			salt
		) VALUES (
			%(firstLastname)s, 
			%(secondLastname)s, 
			%(firstname)s, 
			%(accessLevel)s, 
			%(cellphone)s, 
			%(zipCode)s, 
			%(street)s, 
			%(neighborhood)s, 
			%(addressNumber)s, 
			%(username)s, 
			%(password)s, 
			%(salt)s			
		);
	"""

	update_staff = """
		UPDATE 
			cetac_staff
		SET 
			first_lastname = %(firstLastname)s,
			second_lastname = %(secondLastname)s, 
			firstname = %(firstname)s, 
			username = %(username)s, 
			access_level = %(accessLevel)s, 
			cellphone = %(cellphone)s, 
			zip_code = %(zipCode)s, 
			street = %(street)s, 
			neighborhood = %(neighborhood)s, 
			address_number = %(addressNumber)s
		WHERE 
			id = %(staffId)s
	"""

	delete_staff = """
		DELETE FROM 
			cetac_staff
		WHERE
			id = %(staff_id)s
	"""
