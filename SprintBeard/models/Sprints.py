import binascii
import datetime
import MySQLdb
import uuid
from uuid import UUID

db = MySQLdb.connect(host='localhost', user='dev', passwd='dev', db='agile')

class Sprint:
	'''
	A class that holds data about a Sprint.
		field: string id - the id of the Sprint
		field: datetime start - the start date of the sprint
		field: datetime end - the ending date of the sprint
		field: string board_id - the id of the board the sprint belongs to
	'''
	def __init__(self, id, start, end, board_id):
		self.id = id
		self.start = start
		self.end = end
		self.board_id = board_id

def create(start, end, board_id):
	'''
	Create a new sprint belonging to a board
		arg: start - the starting date of the sprint
		arg: end - the ending date of the sprint
		arg: board_id - the id of the board to add to
	'''

	id = uuid.uuid4()
	print id
	board_id = UUID(board_id)
	#start = start.strftime('%Y-%m-%d')
	#end = end.strftime('%Y-%m-%d')

	cursor = db.cursor()
	cursor.execute('''
			INSERT INTO `sprints` (`id`, `start`, `end`, `board_id`)
			VALUES (%s, %s, %s, %s)
		''',
		(id.bytes, start, end, board_id.bytes)
	)

	try:
		db.commit()
	except:
		db.rollback()

def get_current_sprint(board_id):
	'''
	Get the current sprint for a board.
		arg: board_id - the id of the board to find the sprint for

		return: the current sprint or None if there is no current sprint.
	'''

	now = datetime.datetime.now()#.strftime('%Y-%m-%d')
	board_id = UUID(board_id)

	cursor = db.cursor()
	cursor.execute('''
			SELECT `id`, `start`, `end`, `board_id` FROM `sprints`
			WHERE `start` < %s AND `end` > %s
		''',
		(now, now)
	)

	row = cursor.fetchone()
	sprint = None
	if row is not None:
		sprint = Sprint(binascii.b2a_hex(row[0]), row[1], row[2], row[3])
	return sprint