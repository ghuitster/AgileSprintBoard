import MySQLdb
import uuid
from uuid import UUID

OWNER_PRIVILEGES = 0
ADMIN_PRIVILEGES = 1
EDITOR_PRIVILEGES = 2
VIEWER_PRIVILEGES = 3

db = MySQLdb.connect(host='localhost', user='dev', passwd='dev', db='agile')

class AccessRule:
	'''
	A class that holds information about an access rule.

		field: string user_id - the id of the user this rule is for
		field: string board_id - the id of the board this rule is for
		field: int privileges - the level of privileges the user has. Use the constants defined in
			this module.
	'''
	def __init__(user_id, board_id, privileges):
		self.user_id = user_id
		self.board_id = board_id
		self.privileges = privileges

def create(user_id, board_id, privileges):
	'''
	Create an access rule for a given user on a given board
		arg: user_id - the id of the user to give access to
		arg: board_id - the id of the board to give access to
		arg: privileges - the privilege level to give the user
	'''
	
	user_id = UUID(user_id)
	board_id = UUID(board_id)

	cursor = db.cursor()
	cursor.execute('''
			INSERT INTO `users_boards` (`user_id`, `board_id`, `privileges`)
			VALUES (%s, %s, %s)
			ON DUPLICATE KEY UPDATE `privileges`=%s
		''',
		(user_id.bytes, board_id.bytes, privileges, privileges)
	)

	try:
		db.commit()
	except:
		db.rollback()

def get_by_board(board_id):
	'''
	Get all the access rules for a particular board
		arg: board_id - the id of the board for which to get access rules

		return: a List of AccessRule objects corresponding to the requested board
	'''

	board_id = UUID(board_id)

	cursor = db.cursor()
	cursor.execute('''
			SELECT `user_id`, `board_id`, `privileges`
			FROM `users_boards`
			WHERE `board_id`=%s
		''',
		(board_id.bytes)
	)

	rows = cursor.fetchall()
	access_rules = []
	for row in rows:
		access_rules.append(AccessRule(row[0], row[1], row[2]))
	return access_rules