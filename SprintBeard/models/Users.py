import binascii
import MySQLdb
import uuid
from uuid import UUID

class User:
	'''This class just holds data about a user, namely its name and uuid.'''
	def __init__(self, name, email, id = uuid.uuid4()):
		self.id = id
		self.name = name
		self.email = email

db = MySQLdb.connect(host='localhost', user='dev', passwd='dev', db='agile')

def create(name, email):
	'''
	Add a new user to the database.
		arg: name - the name of the user to insert
		arg: email - the email of the user to insert

		return: the created User
	'''

	user = User(name, email)

	cursor = db.cursor()
	cursor.execute('''
			INSERT INTO `users` (id, name, email)
			VALUES (%s, %s, %s)
		''',
		(user.id.bytes, user.name, user.email)
	)

	try:
		db.commit()
		return user
	except:
		db.rollback()

def get(user_id):
	'''
	Select a user from the database by id
		arg: user_id - the id of the user to find

		return: an User object representing the found user or None if not found
	'''
	user_id = UUID(user_id)

	cursor = db.cursor()
	cursor.execute('''
			SELECT `id`, `name`, `email`
			FROM `users`
			WHERE `id`=%s
		''',
		(id.bytes)
	)

	user = None
	row = cursor.fetchone()
	if row is not None:
		user = User(row[1], row[2], binascii.b2a_hex(row[0]))
	return user

def create_openid_association(userid, openid):
	'''
	Create an association between a user and an openid
		arg: userid - the id (as uuid) of the user for whom to create an association
		arg: openid - the openid to associate
	'''

	cursor = db.cursor()
	cursor.execute('''
			INSERT INTO `users_openids` (`user_id`, `openid`)
			VALUES(%s, %s)
		''',
		(userid.bytes, openid)
	)

	try:
		db.commit()
	except:
		db.rollback()

def get_by_openid(openid):
	'''
	Select a user from the database by openid
		arg: openid - the openid identifier of the user to find

		return: an User object representing the found user or None if not found
	'''

	cursor = db.cursor()
	cursor.execute('''
			SELECT `user_id`
			FROM `users_openids`
			WHERE `openid`=%s
		''',
		(openid)
	)

	user = None
	row = cursor.fetchone()
	if row is not None:
		user = get(UUID(binascii.b2a_hex(row[0])))
	return user