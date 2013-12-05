import MySQLdb
import uuid
from uuid import UUID

db = MySQLdb.connect(host='localhost', user='dev', passwd='dev', db='agile')

def create(story_id, name, description, estimate):
	'''
	Create a new task belonging to a story
		arg: story_id - the id that the task should belong to
		arg: name - the name of the new task
		arg: description - a description of the task
		arg: estimate - the estimated hours to complete the task
	'''
	task_id = uuid.uuid4()
	story_id = UUID(story_id)

	cursor = db.cursor()
	cursor.execute('''
			INSERT INTO `tasks` (`id`, `story_id`, `name`, `description`, `estimate`)
			VALUES (%s, %s, %s, %s, %s)
		''',
		(task_id.bytes, story_id.bytes, name, description, estimate)
	)

	try:
		db.commit()
	except:
		db.rollback()

