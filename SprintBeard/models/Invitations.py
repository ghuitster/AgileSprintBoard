import Boards
import MySQLdb
import uuid

db = MySQLdb.connect(host='localhost', user='dev', passwd='dev', db='agile')

def invite(user_id, board_id, privileges):
	'''
	Invite a user to a board with a specific privilege level. Inviting a user to a board that they've already been invited to in the past will effectively generate a new invitation by resetting the invitation to active.
		arg: user_id - the id of the user to create the invitation for
		arg: board_id - the board to invite the user to
		arg: privileges - the privilege level to give the user. use the constants defined in Boards module to define this parameter
	'''
	invite_id = uuid.uuid4()
	print invite_id
	print invite_id.bytes

	cursor = db.cursor()
	cursor.execute('''
			INSERT INTO `invitations` (`id`, `user_id`, `board_id`, `privileges`)
			VALUES (%s, %s, %s, %s)
			ON DUPLICATE KEY UPDATE `privileges`=%s, `active`=TRUE
		''',
		(invite_id.bytes, user_id, board_id, privileges, privileges)
	)

	try:
		db.commit()
	except:
		db.rollback()

def respond_to_invite(invite_id, accept):
	'''
	Respond to an invitation to a board. If the user accepted the request, add an access rule to the database.
		arg: invite_id - the id of the invitation as a string
		arg: accept - whether to accept the invitation
	'''
	
	cursor = db.cursor()
	cursor.execute('''
			UPDATE `invitations`
			SET `active`=FALSE
			WHERE `id`=%s
		''',
		(invite_id)
	)


	try:
		db.commit()
	except:
		db.rollback()
