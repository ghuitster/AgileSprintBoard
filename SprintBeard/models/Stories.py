import MySQLdb
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
	'''
	def __init__(id, name, description, estimate, board_id, sprint_id = None):
		self.id = id
		self.name = name
		self.description = description
		self.estimate = estimate
		self.board_id = board_id
		self.sprint_id = sprint_id

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
			row[0],
			row[1],
			row[2],
			float(row[3]),
			row[4],
			row[5]
		)

	return story
