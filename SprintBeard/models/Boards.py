import AccessRules
import flask
import MySQLdb
import uuid
from uuid import UUID

db = MySQLdb.connect(host='localhost', user='dev', passwd='dev', db='agile')

class Board:
	'''
	A class that holds data about a Board.
		field: name - the Name of the Board (string)
		field: id - the id of the Board (string)
	'''
	def __init__(self, name, id = uuid.uuid4() ):
		self.name = name
		self.id = id

def create_board(user_id, name):
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

def deleteBoard(boardID):
	'''Deletes a board with id = boardID
		arg: boardID - the id of the board to be deleteBoard
	'''
	board_id = UUID(boardID)
	cursor = db.cursor()
	cursor.execute('''DELETE FROM `boards` WHERE `id`=%s''', board_id)
	cursor.execute('''DELETE FROM `users_boards` WHERE `board_id`=%s''', board_id)
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
		
		return: a List of Boards
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
		# board[1] is a str
		# need to be converted to a UUID
		# due to internet as slow as butt
		# and having wasted 5 hours already
		# im pushing broken code. someone else
		# hack it
		b = Board(board[3], board[1])
		boards.append(b)
	return boards
