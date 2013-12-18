import binascii
import datetime
from Model import check_uuid, cursor, db
import time
import uuid
from uuid import UUID

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

@check_uuid
def create(start, end, board_id):
	'''
	Create a new sprint belonging to a board
		arg: start - the starting date of the sprint
		arg: end - the ending date of the sprint
		arg: board_id - the id of the board to add to
	'''

	id = uuid.uuid4()
	board_id = UUID(board_id)
	#start = start.strftime('%Y-%m-%d')
	#end = end.strftime('%Y-%m-%d')

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

@check_uuid
def get(sprint_id):
	'''
	Get the requested sprint
		arg: sprint_id - the id of the sprint to get

		return: the requested sprint as a Sprint object
	'''
	if sprint_id is None:
		return None

	sprint_id = UUID(sprint_id)

	cursor.execute('''
			SELECT `id`, `start`, `end`, `board_id`
			FROM `sprints`
			WHERE `id`=%s	
		''',
		(sprint_id.bytes)
	)

	row = cursor.fetchone()
	sprint = None
	if row is not None:
		sprint = Sprint(binascii.b2a_hex(row[0]), row[1], row[2], row[3])
	return sprint

@check_uuid
def get_current_sprint(board_id):
	'''
	Get the current sprint for a board.
		arg: board_id - the id of the board to find the sprint for

		return: the current sprint or None if there is no current sprint.
	'''

	now = datetime.datetime.now()#.strftime('%Y-%m-%d')
	board_id = UUID(board_id)

	cursor.execute('''
			SELECT `id`, `start`, `end`, `board_id` FROM `sprints`
			WHERE `start` < %s AND `end` > %s AND `board_id`=%s
		''',
		(now, now, board_id.bytes)
	)

	row = cursor.fetchone()
	sprint = None
	if row is not None:
		sprint = Sprint(binascii.b2a_hex(row[0]), row[1], row[2], row[3])
	return sprint

@check_uuid
def change_dates(sprint_id, start, end):
	'''
	Change the start and end date of the sprint.
		arg: sprint_id - the id of the sprint
		arg: start - the start date of the sprint (MM-DD-YYYY)
		arg: end - the end date of the sprint (MM-DD-YYYY)
	'''

	sprint_id = UUID(sprint_id)
	start = datetime.datetime(*time.strptime(start, '%m-%d-%Y')[0:6])
	end = datetime.datetime(*time.strptime(end, '%m-%d-%Y')[0:6])

	cursor.execute('''
			UPDATE `sprints`
			SET `start`=%s, `end`=%s
			WHERE `id`=%s
		''',
		(start, end, sprint_id.bytes)
	)

	try:
		db.commit()
	except:
		db.rollback()
