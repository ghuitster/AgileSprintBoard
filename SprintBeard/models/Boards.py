import AccessRules
import binascii
import datetime
from dateutil.relativedelta import relativedelta
from Model import check_uuid, cursor, db
import Sprints
import Stories
import Users
import uuid
from uuid import UUID

class Board:
	'''
	A class that holds data about a Board.
		field: string name - the Name of the Board (string)
		field: string id - the id of the Board (string)
		field: List[User] - a list of users that have access to the board
		field: List[Story] - a list of stories that belong to the board
		field: Sprint sprint - the sprint to show
	'''
	def __init__(self, name, id, users=[], stories=[], sprint=None):
		self.name = name
		self.id = id
		self.users = users
		self.stories = stories
		self.sprint = sprint

@check_uuid
def create(user_id, name):
	'''
	Create a Board for a certain userID
		arg: user_id - the id of the user creating the board
		arg: name - the name of the new board
		return: the created board
	'''

	board = Board(name, uuid.uuid4())

	user_id = UUID(user_id)

	cursor.execute('''
			INSERT INTO `boards` (`id`, `name`) 
			VALUES (%s, %s)
		''',
		(board.id.bytes, board.name)
	)
	cursor.execute('''
			INSERT INTO `users_boards` (`user_id`, `board_id`, `privileges`)
			VALUES (%s, %s, %s) 
			ON DUPLICATE KEY UPDATE `privileges`=%s
		''', 
		(user_id.bytes, board.id.bytes, AccessRules.OWNER_PRIVILEGES, AccessRules.OWNER_PRIVILEGES)
	)

	try:
		db.commit()

		#if that succeeded, we'll create a new sprint to start out with
		now = datetime.datetime.now()
		later = now + relativedelta(weeks=4)
		Sprints.create(now, later, board.id.hex)

		return board
	except:
		db.rollback()

@check_uuid
def view(board_id, sprint_id='current'):
	'''
	Get the data for a board in a Board object
		arg: board_id - the id of the board to get
		arg: sprint_id - the id of a sprint belonging to the board for which to get stories.
			Passing in 'all' gets stories from all sprints, passing in 'current' gets
			all stories in the current sprint, and passing in 'backlog' gets all stories in the 
			backlog.
		return: the data in a Board object
	'''

	board_id_uuid = UUID(board_id)
	sprint = None
	if sprint_id == 'current':
		sprint = Sprints.get_current_sprint(board_id)
		if sprint is not None:
			sprint_id = sprint.id
		if sprint is None:
			now = datetime.datetime.now()#.strftime('%Y-%m-%d')
			later = now + relativedelta(weeks=2)#.strftime('%Y-%m-%d')
			sprint = Sprints.create(now, later, board_id)

	elif sprint_id != 'all' and sprint_id != 'backlog':
		sprint_id = UUID(sprint_id).hex
		sprint = Sprints.get(sprint_id)

	cursor.execute('''
			SELECT `name`, `id`
			FROM `boards`
			WHERE `id`=%s
		''',
		(board_id_uuid.bytes)
	)

	row = cursor.fetchone()
	board = None
	if row is not None:
		board = Board(row[0], binascii.b2a_hex(row[1]), Users.get_by_board(board_id), Stories.get_by_board(board_id, sprint_id), sprint)

	return board

@check_uuid
def delete(board_id):
	'''
	Deletes a board with id = board_id
		arg: board_id - the id of the board to be deleted
	'''
	board_id = UUID(board_id)
	cursor.execute('''
			DELETE FROM `boards` 
			WHERE `id`=%s
		''', 
		(board_id.bytes)
	)
	cursor.execute('''
			DELETE FROM `users_boards` 
			WHERE `board_id`=%s
		''',
		(board_id.bytes)
	)
	cursor.execute('''
			DELETE FROM `invitations` 
			WHERE `board_id`=%s
		''',
		(board_id.bytes)
	)
	cursor.execute('''
			DELETE FROM `sprints` 
			WHERE `board_id`=%s
		''',
		(board_id.bytes)
	)
	try:
		db.commit()
	except:
		db.rollback()

	cursor.execute('''
			SELECT `id` FROM `stories` 
			WHERE `board_id`=%s
		''',
		(board_id.bytes)
	)

	story_ids = cursor.fetchall()

	for story in story_ids:
		cursor.execute('''
				DELETE FROM `users_stories` 
				WHERE `story_id`=%s
			''',
			(story[0])
		)
		cursor.execute('''
				DELETE FROM `stories` 
				WHERE `id`=%s
			''',
			(story[0])
		)
		try:
			db.commit()
		except:
			db.rollback()

		cursor.execute('''
				SELECT `id` FROM `tasks` 
				WHERE `story_id`=%s
			''',
			(story[0])
		)

		task_ids = cursor.fetchall()

		for task in task_ids:
			cursor.execute('''
					DELETE FROM `users_tasks` 
					WHERE `task_id`=%s
				''',
				(task[0])
			)
			cursor.execute('''
					DELETE FROM `tasks` 
					WHERE `id`=%s
				''',
				(task[0])
			)
			try:
				db.commit()
			except:
				db.rollback()

@check_uuid
def changeName(board_id, new_name):
	'''
	Change the Name attribute of a Board for a certain board_id
		arg: board_id - the id of the Board to be modified
		arg: new_name - the new Name of the Board
	'''
	board_id = UUID(board_id)
	cursor.execute('''
			UPDATE `boards` 
			SET `name`=%s 
			WHERE `id`=%s
		''', 
		(new_name, board_id.bytes)
	)
	try:
		db.commit()
	except:
		db.rollback()

@check_uuid
def get_user_boards(user_id):
	'''
	Return a list of all Boards associated with a userID
		arg: user_id - the id of the user
		
		return: a List of Boards. These boards DO NOT contain any data other than name and id
	'''

	user_id = UUID(user_id)
	cursor.execute(
		'''
			SELECT `user_id`, `board_id`, `privileges`, `name` 
			FROM `users_boards` INNER JOIN `boards` 
			ON `boards`.`id` = `users_boards`.`board_id` 
			WHERE users_boards.user_id=%s
		''', 
		(user_id.bytes)
	)
	
	boards = []
	user_boards = cursor.fetchall()
	for board in user_boards:
		b = Board(board[3], binascii.b2a_hex(board[1]))
		boards.append(b)
	return boards

@check_uuid
def get(board_id):
	'''
	Get the basic information about a Board, ie, just its name and id.
		arg: board_id - the id of the board to look up

		return: a Board object with name and id.
	'''

	board_id = UUID(board_id)
	cursor.execute('''
			SELECT `id`, `name`
			FROM `boards`
			WHERE `id`=%s
		''',
		(board_id.bytes)
	)

	row = cursor.fetchone()
	board = None
	if row is not None:
		board = Board(row[1], binascii.b2a_hex(row[0]))

	return board
	
@check_uuid
def getRights(board_id, user_id):
	'''
	Get the rights of a user for a board. This will be used to determine whether to 
	display the Board Admin menu on screen.
		arg: board_id - The board to check
		arg: user_id - The user to be checked
		return: The right associated with the user id AND board id
	'''
	user_id = UUID(user_id)
	board_id = UUID(board_id)
	cursor.execute('''
			SELECT `privileges`
			FROM `users_boards`
			WHERE `board_id`=%s
			AND `user_id`=%s
		''',
		(board_id.bytes, user_id.bytes)
	)
	rights = cursor.fetchone()
	return rights[0]
