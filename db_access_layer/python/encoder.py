import json
from datetime import datetime, date


class DateTimeEncoder(json.JSONEncoder):
	"""
	Subclass of the default JSON encoder to properly encode date and datetime objects.
	"""
	def default(self, obj):
		if isinstance(obj, datetime):
			return obj.strftime("%Y-%m-%d %H:%M:%D")

		elif isinstance(obj, date):
			return obj.strftime("%Y-%m-%d")

		else:
			return super().default(obj)
