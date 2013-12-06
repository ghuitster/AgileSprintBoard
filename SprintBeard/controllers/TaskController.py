from auth import Auth
from custom_render.CustomRender import render_view
from flask import Blueprint, render_template, request
from models import Tasks

tasks = Blueprint('tasks', __name__)

@tasks.route('/stories/<story_id>/tasks', methods=['POST'])
@Auth.authorized(Auth.STORY_AUTHORIZATION)
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

	Tasks.create(story_id, name, description, estimate)

	return '{"status": "success"}'
