import AccessRules
import binascii
import flask
import MySQLdb
import Sprints
import Stories
import Users
import uuid
from uuid import UUID

db = MySQLdb.connect(host='localhost', user='dev', passwd='dev', db='agile')

class Board:
	'''
	A class that holds data about a Board.
		field: string name - the Name of the Board (string)
		field: string id - the id of the Board (string)
		field: List[User] - a list of users that have access to the board
		field: List[Story] - a list of stories that belong to the board
	'''
	def __init__(self, name, id = uuid.uuid4(), users=[], stories=[]):
		self.name = name
		self.id = id
		self.users = users
		self.stories = stories

def create(user_id, name):
	'''
	Create a Board for a certain userID
		arg: user_id - the id of the user creating the board
		arg: name - the name of the new board

		return: the created board
	'''

	board = Board(name)
	user_id = UUID(user_id)

	cursor = db.cursor()
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
		return board
	except:
		db.rollback()

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
	if sprint_id == 'current':
		sprint_id = Sprints.get_current_sprint(board_id).id
	elif sprint_id != 'all' and sprint_id != 'backlog':
		sprint_id = UUID(sprint_id).hex

	cursor = db.cursor()
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
		board = Board(row[0], binascii.b2a_hex(row[1]), Users.get_by_board(board_id), Stories.get_by_board(board_id, sprint_id))

	return board

def delete(board_id):
	'''
	Deletes a board with id = board_id
		arg: board_id - the id of the board to be deleted
	'''
	board_id = UUID(board_id)
	
	cursor = db.cursor()
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
	
	try:
		db.commit()
	except:
		db.rollback()

def changeName(boardID, newName):
	'''
	Change the Name attribute of a Board for a certain boardID
		arg: boardID - the id of the Board to be modified
		arg: newName - the new Name of the Board
	'''
	cursor = db.cursor()
	cursor.execute('''UPDATE boards SET name=%s WHERE id=%s''', (newName, boardID))
	try:
		db.commit()
	except:
		db.rollback()

def get_user_boards(user_id):
	'''
	Return a list of all Boards associated with a userID
		arg: user_id - the id of the user
		
		return: a List of Boards. These boards DO NOT contain any data other than name and id
	'''

	user_id = UUID(user_id)
	
	cursor = db.cursor()
	cursor.execute('''
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
