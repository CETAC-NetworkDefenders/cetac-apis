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
        %(firstLastname)s,
        %(secondLastname)s,
        %(firstname)s,
        %(gender)s,
        %(maritalStatus)s,
        %(phone)s,
        %(cellphone)s,
        %(birthDate)s,
        %(birthPlace)s,
        %(occupation)s,
        %(religion)s,
        %(zipCode)s,
        %(street)s,
        %(addressNumber)s
    );
    """

    update_user = """
    UPDATE
        cetac_user
    SET
        first_lastname = %(firstLastname)s,
        second_lastname = %(secondLastname)s,
        firstname = %(firstname)s,
        gender = %(gender)s,
        marital_status = %(maritalStatus)s,
        phone = %(phone)s,
        cellphone = %(cellphone)s,
        birth_date = %(birthDate)s,
        birth_place = %(birthPlace)s,
        occupation = %(occupation)s,
        religion = %(religion)s,
        zip_code = %(zipCode)s,
        street = %(street)s,
        address_number = %(addressNumber)s
    WHERE
        id = %(userId)s
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