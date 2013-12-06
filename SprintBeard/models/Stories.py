import binascii
import MySQLdb
import Tasks
import uuid
from uuid import UUID

db = MySQLdb.connect(host='localhost', user='dev', passwd='dev', db='agile')

class Story:
	'''
	A class that contains data about a story.
		field: string id - the id of this story
		field: string name: the name of this story
		field: string description: a description of the story
		field: float estimate: the number of story points to complete the story
		field: string board_id - the id of the board the story belongs to
		field: string sprint_id - the id of the sprint the story is on, or None if it's on the backlog
		field: List[Task] tasks - a list of tasks that belong to the story
	'''
	def __init__(self, id, name, description, estimate, board_id, sprint_id=None, tasks=[]):
		self.id = id
		self.name = name
		self.description = description
		self.estimate = estimate
		self.board_id = board_id
		self.sprint_id = sprint_id

def create(name, description, estimate, board_id, sprint_id):
	'''
	Create a new story in a board.
		arg: name - the name of the new story
		arg: description - a description for the new story
		arg: estimate - an estimate for story points
		arg: board_id - the id of the board to add to
		arg: sprint_id - the id of the sprint to add to
	'''

	story_id = uuid.uuid4()
	board_id = UUID(board_id)
	if sprint_id is not None:
		sprint_id = UUID(sprint_id).bytes

	cursor = db.cursor()
	cursor.execute('''
			INSERT INTO `stories` (`id`, `name`, `description`, `estimate`, `board_id`, `sprint_id`)
			VALUES (%s, %s, %s, %s, %s, %s)
		''',
		(story_id.bytes, name, description, estimate, board_id
			.bytes, sprint_id)
	)

	try:
		db.commit()
	except:
		db.rollback()

def get(story_id):
	'''
	Get a story out of the database.
		arg: story_id - the id of the story to get out of the database

		return: a Story object containing data about the story
	'''

	story_id = UUID(story_id)

	cursor = db.cursor()
	cursor.execute('''
			SELECT `id`, `name`, `description`, `estimate`, `board_id`, `sprint_id`
			FROM `stories`
			WHERE `id`=%s
		''',
		(story_id.bytes)
	)

	story = None
	row = cursor.fetchone()
	if row is not None:
		story = Story(
			binascii.b2a_hex(row[0]),
			row[1],
			row[2],
			float(row[3]),
			binascii.b2a_hex(row[4]),
			binascii.b2a_hex(row[5])
		)

	return story

def get_by_board(board_id, sprint_id = None):
	'''
	Get the stories for a board.
		arg: board_id - the id of the board to get stories for
		arg: sprint_id - the id of the sprint the stories belong to. 
			Passing in 'all' gets all the stories, and passing in 'backlog' gets backlogged stories
	'''
	board_id = UUID(board_id)
	
	#set up the query dynamically based on the sprint_id passed in
	sql_str = '''
		SELECT `id`, `name`, `description`, `estimate`, `board_id`, `sprint_id`
		FROM `stories`
		WHERE `board_id`=%s
	'''
	sql_tuple = (board_id.bytes)
	if sprint_id != 'all':
		sql_str += ' AND `sprint_id`=%s'

		if sprint_id == 'backlog':
			sql_tuple = (board_id.bytes, None)
		else:
			sql_tuple = (board_id.bytes, UUID(sprint_id).bytes)

	cursor = db.cursor()
	cursor.execute(sql_str, sql_tuple)
	
	rows = cursor.fetchall()
	stories = []
	for row in rows:
		stories.append(Story(
				binascii.b2a_hex(row[0]),
				row[1],
				row[2],
				float(row[3]),
				binascii.b2a_hex(row[4]),
				binascii.b2a_hex(row[5]),
				Tasks.get_by_story(binascii.b2a_hex(row[0]))
			)
		)

	return stories