
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
    'firstLastname': {
        'required': True,
        'type': 'string'
    },
    'secondLastname': {
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
    'maritalStatus': {
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
    'birthDate': {
        'required': True,
        'type': 'string'
    },
    'birthPlace': {
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
    'zipCode': {
        'required': True,
        'type': 'integer'
    },
    'street': {
        'required': True,
        'type': 'string'
    },
    'addressNumber': {
        'required': True,
        'type': 'integer'
    },
}

PATCH_USER_SCHEMA = {
    'userId': {
        'required': True,
        'type': 'integer'
    },
    'firstLastname': {
        'required': True,
        'type': 'string'
    },
    'secondLastname': {
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
    'maritalStatus': {
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
    'birthDate': {
        'required': True,
        'type': 'string'
    },
    'birthPlace': {
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
    'zipCode': {
        'required': True,
        'type': 'integer'
    },
    'street': {
        'required': True,
        'type': 'string'
    },
    'addressNumber': {
        'required': True,
        'type': 'integer'
    },
}
