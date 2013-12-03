import MySQLdb
import uuid
import flask

db = MySQLdb.connect(host='localhost', user='dev', passwd='dev', db='agile')

class Board:						# Class holds NAME and ID for a given Board
	def __init__(self, name, id = uuid.uuid4() ):
		self.name = name
		self.id = id

def createBoard(userID):					# Adds 'default' board to DB. Returns the Board
	board = Board("Default Board");
	cursor = db.cursor()
	cursor.execute('''INSERT INTO boards (id, name) VALUES (%s, '%s')''', (board.id.bytes, board.name) )
	cursor.execute('''INSERT INTO users_boards (user_id, board_id) VALUES (%s, %s)''', (userID.id.bytes, board.id.bytes) )
	try:
		db.commit()
		return board
	except:
		db.rollback()

def changeName(boardID, newName):	# Changes the Name of a Board in the DB
	cursor = db.cursor()
	cursor.execute('''UPDATE boards SET name=%s WHERE id=%s''', (newName, boardID))
	try:
		db.commit()
	except:
		db.rollback()

def getUserBoards(userID):			# get all the boards for the user
	cursor = db.cursor()
	userBoards = cursor.execute('''select user_id, board_id, privileges, name from users_boards inner join boards on boards.id = users_boards.board_id where users_boards.user_id="%s"''', (userID))
	
	boards = []
	for board in userBoards:
		b = Board(board[3], board[1])
		boards.append(b)
	return boards
