from enum import Enum

class UserQueries(Enum):
    get_user = """
    SELECT
        *
    FROM 
        cetac_user
    WHERE 
        id = %(user_id)s
    """

    create_user = """
    INSERT INTO
        cetac_user
    (
        first_lastname,
        second_lastname,
        firstname,
        gender,
        marital_status,
        phone,
        cellphone,
        birth_date,
        birth_place,
        occupation,
        religion,
        zip_code,
        street,
        address_number
    ) VALUES (
        %(first_lastname)s,
        %(second_lastname)s,
        %(firstname)s,
        %(gender)s,
        %(marital_status)s,
        %(phone)s,
        %(cellphone)s,
        %(birth_date)s,
        %(birth_place)s,
        %(occupation)s,
        %(religion)s,
        %(zip_code)s,
        %(street)s,
        %(address_number)s
    ) RETURNING id;
    """

    update_user = """
    UPDATE
        cetac_user
    SET
        first_lastname = %(first_lastname)s,
        second_lastname = %(second_lastname)s,
        firstname = %(firstname)s,
        gender = %(gender)s,
        marital_status = %(marital_status)s,
        phone = %(phone)s,
        cellphone = %(cellphone)s,
        birth_date = %(birth_date)s,
        birth_place = %(birth_place)s,
        occupation = %(occupation)s,
        religion = %(religion)s,
        zip_code = %(zip_code)s,
        street = %(street)s,
        address_number = %(address_number)s
    WHERE
        id = %(id)s
    """

    get_user_listing = """
		SELECT 
			first_lastname,
			second_lastname,
			firstname
		FROM 
			cetac_user
	""" 

    get_user_listing_by_staff_id = """
        SELECT DISTINCT
            user_id,
            first_lastname,
            second_lastname,
            firstname
        FROM
            cetac_user
        JOIN
            cetac_record 
        ON 
            cetac_user.id = cetac_record.user_id
        WHERE staff_id = %(staff_id)s;
    """