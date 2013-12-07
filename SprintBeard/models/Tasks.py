import binascii
import MySQLdb
import uuid
from uuid import UUID

db = MySQLdb.connect(host='localhost', user='dev', passwd='dev', db='agile')

class Task:
	'''
	A class that holds data about a Task.
		field: string id - the id of the task
		field: string story_id - the id of the story the task belongs to
		field: string name - the name of the task
		field: string description - description of the task
		field: float estimate - the estimated number of hours to complete the task
		field: bool completed - whether the task has been completed
		field: datetime completion_date - the time when the task was completed
	'''
	def __init__(self, id, story_id, name, description, estimate, completed = False, \
			completion_date = None):
		self.id = id
		self.story_id = story_id
		self.name = name
		self.description = description
		self.estimate = estimate
		self.completed = completed
		self.completion_date = completion_date


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

def get(task_id):
	'''
	Get a task by its id
		arg: task_id - the id of the task to get

		return: the task data in a Task object
	'''
	
	task_id = UUID(task_id)

	cursor = db.cursor()
	cursor.execute('''
			SELECT `id`, `story_id`, `name`, `description`, `estimate`, `completed`, `completion_date`
			FROM `tasks`
			WHERE `id`=%s
		''',
		(task_id.bytes)
	)

	task = None
	row = cursor.fetchone()
	if row is not None:
		task = Task(
			binascii.b2a_hex(row[0]),
			binascii.b2a_hex(row[1]),
			row[2],
			row[3],
			float(row[4]),
			bool(row[5]),
			row[6]
		)

	return task

def delete(task_id):
	'''
	Delete a task.
		arg: task_id - the id of the task to delete
	'''

	task_id - UUID(task_id)

	cursor = db.cursor()
	cursor.execute('''
			DELETE FROM `tasks`
			WHERE `task_id`=%s
		''',
		(task_id.bytes)
	)

	try:
		db.commit()
	except:
		db.rollback()

def get_by_story(story_id):
	'''
	Get all tasks belonging to a particular story
		arg: story_id = the id of the story to get tasks for

		return: a List of Task objects containing all the task data
	'''

	story_id = UUID(story_id)

	cursor = db.cursor()
	cursor.execute('''
			SELECT `id`, `story_id`, `name`, `description`, `estimate`, `completed`, `completion_date`
			FROM `tasks`
			WHERE `story_id`=%s
		''',
		(story_id.bytes)
	)

	rows = cursor.fetchall()
	tasks = []
	for row in rows:
		tasks.append(Task(
				binascii.b2a_hex(row[0]),
				binascii.b2a_hex(row[1]),
				row[2],
				row[3],
				float(row[4]),
				bool(row[5]),
				row[6]
			)
		)
	return tasks
