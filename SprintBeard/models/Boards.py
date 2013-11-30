import MySQLdb
import uuid
from uuid import UUID

ADMIN_PRIVILEGES = 0
EDITOR_PRIVILEGES = 1
VIEWER_PRIVILEGES = 2

db = MySQLdb.connect(host='localhost', user='dev', passwd='dev', db='agile')

def create_access_rule(user_id, board_id, privileges):
	'''
	Create an access rule to a certain board for a particular user.
		arg: user_id - the id of the user for whom to add a rule
		arg: board_id - the id of the board they gain access to
		arg: privileges - the privilege level they gain (use the constants in this module)
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
