import MySQLdb
import uuid
import flask
from uuid import UUID
import AccessRules

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

def createBoard(userID):
	'''
	Create a Board for a certain userID
		arg: userID - the id of the user creating the board
		return: a Default Board
	'''
	board = Board("Default Board");
	user_id = UUID(userID)
	cursor = db.cursor()
	cursor.execute('''INSERT INTO `boards` (`id`, `name`) VALUES (%s, %s)''', (board.id.bytes, board.name) )
	cursor.execute('''INSERT INTO `users_boards` (`user_id`, `board_id`, `privileges`) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE `privileges`=%s''', (user_id.bytes, board.id.bytes, AccessRules.OWNER_PRIVILEGES, AccessRules.OWNER_PRIVILEGES))
	try:
		db.commit()
		return board
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

def getUserBoards(userID):
	'''
	Return a list of all Boards associated with a userID
		arg: userID - the id of the user
		
		return: a List of Boards
	'''
	cursor = db.cursor()
	user_id = UUID(userID)
	cursor.execute('''SELECT `user_id`, `board_id`, `privileges`, `name` FROM `users_boards` INNER JOIN `boards` ON boards.id = users_boards.board_id WHERE users_boards.user_id=%s''', (user_id.bytes))
	
	boards = []
	user_boards = cursor.fetchall()
	for board in user_boards:
		b = Board(board[3], board[1])
		boards.append(b)
	return boards
