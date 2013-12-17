import binascii
from Model import check_uuid, db
import uuid
from uuid import UUID

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
			completion_date = None, users = []):
		self.id = id
		self.story_id = story_id
		self.name = name
		self.description = description
		self.estimate = estimate
		self.completed = completed
		self.completion_date = completion_date
		self.users = users


@check_uuid
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

@check_uuid
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

@check_uuid
def delete(task_id):
	'''
	Delete a task.
		arg: task_id - the id of the task to delete
	'''

	task_id = UUID(task_id)

	cursor = db.cursor()
	cursor.execute('''
			DELETE FROM `tasks`
			WHERE `id`=%s
		''',
		(task_id.bytes)
	)

	try:
		db.commit()
	except:
		db.rollback()

@check_uuid
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
				row[6],
				get_users(binascii.b2a_hex(row[0]))
			)
		)
	return tasks

def get_users(task_id):
	'''
	Get all user ids for users assigned to a particular task.
		arg: task_id - the id of the task to search for

		return: a List of String uuids
	'''

	task_id = UUID(task_id)

	cursor = db.cursor()
	cursor.execute('''
			SELECT `user_id`
			FROM `users_tasks`
			WHERE `task_id`=%s
		''',
		(task_id.bytes)
	)

	rows = cursor.fetchall()
	users = []
	for row in rows:
		users.append(binascii.b2a_hex(row[0]))

	return users

@check_uuid
def assign(task_id, user_id):
	'''
	Assign a task to a particular user in the database
		arg: task_id - the id of the task to assign
		arg: user_id - the id of the user to assign to the task
	'''

	task_id = UUID(task_id)
	user_id = UUID(user_id)

	cursor = db.cursor()
	cursor.execute('''
			INSERT INTO `users_tasks` (`task_id`, `user_id`)
			VALUES (%s, %s)
			ON DUPLICATE KEY UPDATE `task_id`=%s
		''',
		(task_id.bytes, user_id.bytes, task_id.bytes)
	)

	try:
		db.commit()
	except:
		db.rollback()

@check_uuid
def unassign(task_id, user_id):
	'''
	Unassign a particular user from a task in the database.
		arg: task_id - the id of the task to unassign
		arg: user_id - the id fo the user to unassign from the task
	'''

	task_id = UUID(task_id)
	user_id = UUID(user_id)

	cursor = db.cursor()
	cursor.execute('''
			DELETE FROM `users_tasks`
			WHERE `task_id`=%s AND `user_id`=%s
		''',
		(task_id.bytes, user_id.bytes)
	)

	try:
		db.commit()
	except:
		db.rollback()
