import simplejson
from simplejson import JSONDecoder, JSONEncoder
from Users import user_from_json

def _default(self, obj):
	return getattr(obj.__class__, "to_json", _default.default)(obj)

_default.default = JSONEncoder().default
JSONEncoder.default = _default

def _decode(self, s):
	decoded = s
	if type(s) is str:
		try:
			decoded = _decode.decode(s.replace('\\', '')[1:-1])
		except:
			pass

	#it was an object, check if it was one of ours
	if (type(decoded) is dict and
		'__class__' in decoded and
		decoded['__class__'] == 'User'):
		return user_from_json(decoded)
	#it wasn't of our object type, just do default
	elif type(decoded) is str:
		return _decode.decode(s)
	#it wasn't even a string to begin with, just return what was passed in
	else:
		return s

_decode.decode = JSONDecoder().decode
JSONDecoder.decode = _decode
