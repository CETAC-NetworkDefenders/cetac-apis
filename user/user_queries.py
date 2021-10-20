from enum import Enum

from user.app import update_record


class UserQueries(Enum):
    get_user = """
        SELECT
            cetac_user.*, 
            cetac_record.id as record_id
        FROM 
            cetac_user
        INNER JOIN 
            cetac_record
        ON cetac_user.id = cetac_record.user_id
        WHERE 
            cetac_user.id = %(user_id)s
    """

    create_user = """
        WITH inserted_user AS (
            INSERT INTO cetac_user(
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
            ) RETURNING id
        ) INSERT INTO cetac_record (
            staff_id, 
            user_id, 
            ekr, 
            is_open
        ) VALUES(
            %(staff_id)s, 
            (SELECT id from inserted_user), 
            'EKR DE PRUEBA',
            TRUE
        )
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
            cetac_user.id, 
            cetac_record.id AS record_id, 
            first_lastname,
            second_lastname,
            firstname,
            birth_date
        FROM 
            cetac_user
        INNER JOIN 
            cetac_record
        ON 	
            cetac_record.user_id = cetac_user.id
        WHERE 
            cetac_record.is_open = FALSE
	"""

    get_user_listing_by_staff_id = """
        SELECT DISTINCT
            user_id,
            cetac_record.id AS record_id, 
            first_lastname,
            second_lastname,
            firstname
        FROM
            cetac_user
        JOIN
            cetac_record 
        ON 
            cetac_user.id = cetac_record.user_id
        WHERE 
            cetac_record.staff_id = %(staff_id)s AND 
            cetac_record.is_open = TRUE;
    """

    update_record = """
        UPDATE
            cetac_record
        SET
            staff_id = %(staff_id)s, is_open = true
        WHERE
            id = %(record_id)s
    """
