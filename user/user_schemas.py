
GET_USER_SCHEMA = {
    'userId': {
        'required': True,
    }
}

GET_USER_LISTING_SCHEMA = {
    'listing': {
        'required': True,
    },
}

GET_USER_LISTING_BY_STAFF_ID_SCHEMA = {
    'listing': {
        'required': True,
    },
    'staffId': {
        'required': True,
    },
}

POST_USER_SCHEMA = {
    'first_lastname': {
        'required': True,
        'type': 'string'
    },
    'second_lastname': {
        'required': True,
        'type': 'string'
    },
    'firstname': {
        'required': True,
        'type': 'string'
    },
    'gender': {
        'required': True,
        'type': 'string'
    },
    'marital_status': {
        'required': True,
        'type': 'string'
    },
    'phone': {
        'required': True,
        'type': 'string'
    },
    'cellphone': {
        'required': True,
        'type': 'string'
    },
    'birth_date': {
        'required': True,
        'type': 'string'
    },
    'birth_place': {
        'required': True,
        'type': 'string'
    },
    'occupation': {
        'required': True,
        'type': 'string'
    },
    'religion': {
        'required': True,
        'type': 'string'
    },
    'zip_code': {
        'required': True,
        'type': 'string'
    },
    'street': {
        'required': True,
        'type': 'string'
    },
    'address_number': {
        'required': True,
        'type': 'string'
    },
}

PATCH_USER_SCHEMA = {
    'id': {
        'required': True,
        'type': 'integer'
    },
    'first_lastname': {
        'required': True,
        'type': 'string'
    },
    'second_lastname': {
        'required': True,
        'type': 'string'
    },
    'firstname': {
        'required': True,
        'type': 'string'
    },
    'gender': {
        'required': True,
        'type': 'string'
    },
    'marital_status': {
        'required': True,
        'type': 'string'
    },
    'phone': {
        'required': True,
        'type': 'string'
    },
    'cellphone': {
        'required': True,
        'type': 'string'
    },
    'birth_date': {
        'required': True,
        'type': 'string'
    },
    'birth_place': {
        'required': True,
        'type': 'string'
    },
    'occupation': {
        'required': True,
        'type': 'string'
    },
    'religion': {
        'required': True,
        'type': 'string'
    },
    'zip_code': {
        'required': True,
        'type': 'string'
    },
    'street': {
        'required': True,
        'type': 'string'
    },
    'address_number': {
        'required': True,
        'type': 'string'
    },
}
