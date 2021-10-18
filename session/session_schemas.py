
POST_SESSION_SCHEMA = {
	'tool': {
		'required': True,
		'type': 'string'
	},
	'intervention_type': {
		'required': True,
		'type': 'string'
	},
	'evaluation': {
		'required': True,
		'type': 'string'
	},
	'session_date': {
		'required': True,
		'type': 'string'
	},
	'motive': {
		'required': True,
		'type': 'string'
	},
	'service_type': {
		'required': True,
		'type': 'string'
	},
	'recovery_fee': {
		'required': True,
		'type': 'float'
	},
	'record_id': {
		'required': True,
		'type': 'integer'
	},
	'is_open': {
		'required': True,
		'type': 'boolean'
	}
}