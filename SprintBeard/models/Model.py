from functools import wraps
import MySQLdb
from uuid import UUID

db = MySQLdb.connect(host='localhost', user='dev', passwd='dev', db='agile')

def check_uuid(handler):
	'''
	A function decorator that handles the case that UUIDs passed into the original function
	are malformed. If they are, a dictionary containing information about the error is returned.
		arg: handler - the function that takes UUIDs as arguments

		return: the handler augmented such that it will handle malformed UUIDs gracefully
	'''
	@wraps(handler)
	def do_check(*args, **kwargs):
		try:
			return handler(*args, **kwargs)
		except ValueError, e:
			if 'UUID' in str(e):
				return {
					'status': 'failure',
					'error': 'malformed UUID'
				}
			else:
				raise

	return do_check