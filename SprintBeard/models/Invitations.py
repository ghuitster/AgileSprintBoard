import binascii
import Boards
from Model import check_uuid, cursor, db
import uuid
from uuid import UUID
import AccessRules

class Invitation:
	'''
	A class that holds data about an invitation.
		field: string id - the id of this invitation (string)
		field: string user_id - the id of the user this invitation was extended to (string)
		field: string board_id - the id of the board the user is invited to (string)
		field: int privileges - the privilege level accepting the invitation results in (constant defined
			in AccessRules module)
		field: bool active - whether or not the invitation is active (bool)
		field: string board_name - the name of the board the user is invited to
	'''

	def __init__(self, id, user_id, board_id, privileges, active, board_name=None):
		self.id = id
		self.user_id = user_id
		self.board_id = board_id
		self.privileges = privileges
		self.active = active
		self.board_name = board_name

@check_uuid
def get(invite_id):
	'''
	Get the record for a particular invitation
		arg: invite_id - the id of the invitation to get

		return: an Invitation containing the data about the invitation
	'''
	id = UUID(invite_id)
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

@check_uuid
def invite(user_email, board_id, privileges):
	'''
	Invite a user to a board with a specific privilege level. Inviting a user to a board that 
	they've already been invited to in the past will effectively generate a new 
	invitation by resetting the invitation to active.
		arg: user_email - the email of the user to create the invitation for
		arg: board_id - the board to invite the user to
		arg: privileges - the privilege level to give the user. use the constants defined in 
			AccessRules module to define this parameter
	'''
	invite_id = uuid.uuid4()
	board_id = UUID(board_id)

	cursor.execute('''
			SELECT `id` 
			FROM `users` 
			WHERE `email`=%s
		''',
		(user_email)
	)
	
	row = cursor.fetchone()
	user_id = None
	if row is not None:
		user_id = row[0]

	if user_id != None:
		cursor.execute('''
				INSERT INTO `invitations` (`id`, `user_id`, `board_id`, `privileges`)
				VALUES (%s, %s, %s, %s)
				ON DUPLICATE KEY UPDATE `privileges`=%s, `active`=TRUE
			''',
			(invite_id.bytes, user_id, board_id.bytes, privileges, privileges)
		)
		try:
			db.commit()
		except:
			db.rollback()

@check_uuid
def respond_to_invite(invite_id, accept):
	'''
	Respond to an invitation to a board. If the user accepted the request, add an access rule to the
	database.
		arg: invite_id - the id of the invitation as a string
		arg: accept - whether to accept the invitation
	'''

	if accept:
		invitation = get(invite_id)
		if invitation is None or invitation.active == False:
			return

		AccessRules.create(invitation.user_id, invitation.board_id, invitation.privileges)

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

@check_uuid
def get_by_user(user_id):
	'''
	Get all the active invitations for a given user
		arg: user_id - the id of the user to get the invitations for

		return: a List of Invitation objects that belong to the user
	'''

	user_id = UUID(user_id)

	cursor.execute('''
			SELECT `invitations`.`id`, `user_id`, `board_id`, `privileges`, `active`, `name`
			FROM `invitations` INNER JOIN `boards` ON `boards`.`id` = `invitations`.`board_id`
			WHERE `user_id`=%s AND `active`=TRUE
		''',
		(user_id.bytes)
	)

	rows = cursor.fetchall()
	invites = []
	for row in rows:
		invites.append(
			Invitation(
				binascii.b2a_hex(row[0]),
				binascii.b2a_hex(row[1]),
				binascii.b2a_hex(row[2]),
				int(row[3]),
				bool(row[4]),
				row[5]
			)
		)

	return invites
