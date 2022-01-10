MONGO_HOST = 'localhost'
MONGO_PORT = 27017

MONGO_DBNAME = 'team6DB'
RESOURCE_METHODS = ['GET', 'PATCH', 'POST', 'DELETE']
ITEM_METHODS = ['GET', 'PATCH', 'PUT', 'DELETE']

schema = {
	# Schema definition, based on Cerberus grammar. Check the Cerberus project (https://github.com/pyeve/cerberus) for details.
		'logmessage': {
		'type': 'string',
		'minlength': 1,
		'maxlength': 1000,
	},
}

logmessage = {
	# 'title' tag used in item links. Defaults to the resource title minus the final, plural 's' (works fine in most cases but not for 'people')
	'item_title': 'postmessage',
	# by default the standard item entry point is defined as '/people/<ObjectId>'. We leave it untouched, and we also enable an additional
	# read-only entry point. This way consumers can also perform GET requests at '/people/<lastname>'.
	'additional_lookup': {
		'url': 'regex("[\w]+")',
		'field': 'logmessage'
	},
	# We choose to override global cache-control directives for this resource.
	'cache_control': 'max-age=10,must-revalidate',
	'cache_expires': 10,
	# most global settings can be overridden at resource level
	'resource_methods': ['GET', 'POST', 'DELETE'],
	'schema': schema
}

DOMAIN = {
	'logmessage': logmessage
}






