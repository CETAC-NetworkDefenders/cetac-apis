
GET_DELETE_STAFF_SCHEMA = {
	'staff_id': {
		'required': True,
	}
}

GET_STAFF_LISTING_SCHEMA = {
	'listing': {
		'required': True,
	},
	'access_level': {
		'required': True,
		'type': 'string', 'allowed': ['admin', 'thanatologist', 'admin_support']
	},
	'lastname_filter': {
		'required': False,
		'type': 'string'
	}
}

POST_STAFF_SCHEMA = {
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
	'access_level': {
		'required': True,
		'type': 'string'
	},
	'cellphone': {
		'required': True,
		'type': 'string'
	},
	'neighborhood': {
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
		'type': 'integer'
	},
	'username': {
		'required': True,
		'type': 'string'
	},
	'password': {
		'required': True,
		'type': 'string',
	},
	'salt': {
		'required': True,
		'type': 'string',
	}
}

PATCH_STAFF_SCHEMA = {
	'id': {
		'required': True,
		'type': 'integer',
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
	'access_level': {
		'required': False,
		'type': 'string'
	},
	'cellphone': {
		'required': True,
		'type': 'string'
	},
	'neighborhood': {
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
		'type': 'integer'
	}
}
