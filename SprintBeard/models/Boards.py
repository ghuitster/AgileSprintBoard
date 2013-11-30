import MySQLdb
import uuid

ADMIN_PRIVILEGES = 0
EDITOR_PRIVILEGES = 1
VIEWER_PRIVILEGES = 2

db = MySQLdb.connect(host='localhost', user='dev', passwd='dev', db='agile')

class Board:				# Class holds NAME and ID for a given Board
	def __init__(self):
		self.name = "Default Board"
		self.id = id

def createBoard():			# Adds 'default' board to DB. Returns the Board
	board = Board();
	cursor = db.cursor()
	cursor.execute('''INSERT INTO boards (id, name) VALUES (%s, '%s')''', (board.id.bytes, board.name) )
	try:
		db.commit()
		return board
	except:
		db.rollback()

def changeName(boardID, newName):	# Changes the Name of a Board in the DB
	cursor = db.cursor()
	cursor.execute('''UPDATE boards SET name=%s WHERE id=%s''', (newTitle, boardID))
	try:
		db.commit()
	except:
		db.rollback()

