import binascii
import Boards
import MySQLdb
import uuid
from uuid import UUID

db = MySQLdb.connect(host='localhost', user='dev', passwd='dev', db='agile')

class Invitation:
	'''
	A class that holds data about an invitation.
		field: id - the id of this invitation (string)
		field: user_id - the id of the user this invitation was extended to (string)
		field: board_id - the id of the board the user is invited to (string)
		field: privileges - the privilege level accepting the invitation results in (constant defined in Boards module)
		field: active - whether or not the invitation is active (bool)
	'''

	def __init__(self, id, user_id, board_id, privileges, active):
		self.id = id
		self.user_id = user_id
		self.board_id = board_id
		self.privileges = privileges
		self.active = active

def get(invite_id):
	'''
	Get the record for a particular invitation
		arg: invite_id - the id of the invitation to get

		return: an Invitation containing the data about the invitation
	'''
	id = UUID(invite_id)
	cursor = db.cursor()
	cursor.execute('''
			SELECT * FROM `invitations`
			WHERE `id`=%s
		''',
		(id.bytes)
	)

	invitation = None
	row = cursor.fetchone()
	if row is not None:
		invitation = Invitation(
			binascii.b2a_hex(row[0]),
			binascii.b2a_hex(row[1]),
			binascii.b2a_hex(row[2]),
			int(row[3]),
			bool(row[4])
		)
	return invitation


def invite(user_id, board_id, privileges):
	'''
	Invite a user to a board with a specific privilege level. Inviting a user to a board that they've already been invited to in the past will effectively generate a new invitation by resetting the invitation to active.
		arg: user_id - the id of the user to create the invitation for
		arg: board_id - the board to invite the user to
		arg: privileges - the privilege level to give the user. use the constants defined in Boards module to define this parameter
	'''
	invite_id = uuid.uuid4()

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

	if accept:
		invitation = get(invite_id)
		if invitation is None or invitation.active == False:
			return

		Boards.create_access_rule(invitation.user_id, invitation.board_id, invitation.privileges)

	invite_id = UUID(invite_id)
	cursor.execute('''
			UPDATE `invitations`
			SET `active`=FALSE
			WHERE `id`=%s
		''',
		(invite_id.bytes)
	)

	try:
		db.commit()
	except:
		db.rollback()
