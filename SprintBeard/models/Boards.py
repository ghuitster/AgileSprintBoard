import MySQLdb
import uuid
import flask

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
	cursor = db.cursor()
	cursor.execute('''INSERT INTO boards (id, name) VALUES (%s, '%s')''', (board.id.bytes, board.name) )
	cursor.execute('''INSERT INTO users_boards (user_id, board_id) VALUES (%s, %s)''', (userID.id.bytes, board.id.bytes) )
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

def get_user_boards(userID):
	'''
	Return a list of all Boards associated with a userID
		arg: userID - the id of the user
		
		return: a List of Boards
	'''
	cursor = db.cursor()
	cursor.execute('''select user_id, board_id, privileges, name from users_boards inner join boards on boards.id = users_boards.board_id where users_boards.user_id="%s"''', (userID))
	
	boards = []
	user_boards = cursor.fetchall()
	for board in user_boards:
		b = Board(board[3], board[1])
		boards.append(b)
	return boards
