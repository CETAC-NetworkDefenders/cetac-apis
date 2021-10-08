
GET_DELETE_STAFF_SCHEMA = {
	'staffId': {
		'required': True,
	}
}

GET_STAFF_LISTING_SCHEMA = {
	'listing': {
		'required': True,
	},
	'accessLevel': {
		'required': True,
		'type': 'string', 'allowed': ['admin', 'thanatologist', 'admin_support']
	},
	'lastnameFilter': {
		'required': False,
		'type': 'string'
	}
}

POST_STAFF_SCHEMA = {
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
	'accessLevel': {
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
	'zipCode': {
		'required': True,
		'type': 'string'
	},
	'street': {
		'required': True,
		'type': 'string'
	},
	'addressNumber': {
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
	'staffId' : {
		'required': True,
		'type': 'integer',
	},
	'firstLastname' : {
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
	'accessLevel': {
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
	'zipCode': {
		'required': True,
		'type': 'string'
	},
	'street': {
		'required': True,
		'type': 'string'
	},
	'addressNumber': {
		'required': True,
		'type': 'integer'
	},
	'username': {
		'required': True,
		'type': 'string'
	}
}
