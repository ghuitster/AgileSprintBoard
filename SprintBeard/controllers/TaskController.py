from auth import Auth
from custom_render.CustomRender import render_view
from flask import Blueprint, render_template, request
import json
from models import Tasks

tasks = Blueprint('tasks', __name__)

@tasks.route('/stories/<story_id>/tasks', methods=['POST'])
@Auth.authorized(Auth.STORY_AUTHORIZATION, Auth.MALFORMED_UUID_JSON)
def create(story_id):
	'''
	Create a new task in the given story.
		arg: story_id - the id of the story the new task will belong to
		POST arg: name - the name of the task
		POST arg: description - a description of the task
		POST arg: estimate - the estimated hours for the task
	'''
	name = request.form['name']
	estimate = 1.0
	try:
		estimate = float(request.form['estimate'])
	except ValueError:
		estimate = 1.0
	description = ''
	if 'description' in request.form:
		description = request.form['description']

	result = Tasks.create(story_id, name, description, estimate)

	if type(result) != dict:
		return '{"status": "success"}'
	else:
		return json.dumps(result)

@tasks.route('/tasks/<task_id>/edit', methods=['POST'])
@Auth.authorized(Auth.TASK_AUTHORIZATION, Auth.MALFORMED_UUID_JSON)
def edit(task_id):
	'''
	Edits a task in the given board
		arg: task - the id of the task to be edited
		POST arg: name - the name of the task
		POST arg: description - a description of the task
		POST arg: estimate - an estimate of task's man hours to completion
	'''
	name = request.form['name']
	description = request.form['description']
	estimate = 1.0
	try:
		estimate = float(request.form['estimate'])
	except ValueError:
		estimate = 1.0

	result = Tasks.edit(task_id, name, description, estimate)

	if type(result) != dict:
		return '{"status": "success"}'
	else:
		return json.dumps(result)

@tasks.route('/tasks/<task_id>', methods=['DELETE'])
@Auth.authorized(Auth.TASK_AUTHORIZATION, Auth.MALFORMED_UUID_JSON)
def delete(task_id):
	'''
	Delete a task from the database
		arg: task_id - the id of the task to delete
	'''

	Tasks.delete(task_id)
	return '{"status": "success"}'

@tasks.route('/assign/tasks/<task_id>', methods=['POST'])
@Auth.authorized(Auth.TASK_AUTHORIZATION, Auth.MALFORMED_UUID_JSON)
def assign(task_id):
	'''
	Assign a user to a task.
		arg: task_id - the id of the task to assign
		POST arg: user_id - the id of the user to assign to the task
	'''
	
	user_id = request.form['user_id']
	Tasks.assign(task_id, user_id)
	return '{"status": "success"}'

@tasks.route('/assign/tasks/<task_id>', methods=['DELETE'])
@Auth.authorized(Auth.TASK_AUTHORIZATION, Auth.MALFORMED_UUID_JSON)
def unassign(task_id):
	'''
	Unassign a user from a task.
		arg: task_id - the task to unassign from
		POST arg: user_id - the id of the user to unassign from the task
	'''

	user_id = request.form['user_id']
	Tasks.unassign(task_id, user_id)
	return '{"status": "success"}'
