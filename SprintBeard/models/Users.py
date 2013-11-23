import binascii
import MySQLdb
import uuid

class User:
	'''This class just holds data about a user, namely its name and uuid.'''
	def __init__(self, name, id = uuid.uuid4()):
		self.id = id
		self.name = name

db = MySQLdb.connect(host='localhost', user='dev', passwd='dev', db='agile')

def create(name):
	'''
	Add a new user to the database.
		arg: name - the name of the user to insert
	'''

	user = User(name)

	cursor = db.cursor()
	cursor.execute('''
			INSERT INTO `users` (id, name)
			VALUES (%s, %s)
		''',
		(user.id.bytes, user.name)
	)

	try:
		db.commit()
	except:
		db.rollback()

def get(id):
	'''
	Select a user from the database by id
		arg: id - the id of the user to find as a uuid object

		return: a User object representing the found user or None if not found
	'''

	cursor = db.cursor()
	cursor.execute('''
			SELECT `id`, `name`
			FROM `users`
			WHERE `id`=%s
		''',
		(id.bytes)
	)

	user = None
	row = cursor.fetchone()
	if row is not None:
		user = User(row[1], binascii.b2a_hex(row[0]))
	return user