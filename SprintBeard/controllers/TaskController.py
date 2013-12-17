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
	estimate = int(request.form['estimate'])
	description = ''
	if 'description' in request.form:
		description = request.form['description']

	result = Tasks.create(story_id, name, description, estimate)

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
	result = Tasks.assign(task_id, user_id)
	return '{"status": "success"}'
