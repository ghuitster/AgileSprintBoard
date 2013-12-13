from auth import Auth
from custom_render.CustomRender import render_view
from flask import Blueprint, request
import json
from models import Sprints, Stories

stories = Blueprint('stories', __name__)

@stories.route('/boards/<board_id>/stories', methods=['POST'])
@Auth.authorized(Auth.BOARD_AUTHORIZATION, Auth.MALFORMED_UUID_JSON)
def create(board_id):
	'''
	Create a new story in the given board
		arg: board_id - the id of the board to add a story to
		POST arg: name - the name of the story
		POST arg: description - a description of the story
		POST arg: estimate - an estimate of story points
		POST arg: sprint_id - the id of the sprint to add to, 'backlog' for backlog,
			or 'current' for the current sprint
	'''
	name = request.form['name']
	description = request.form['description']
	estimate = float(request.form['estimate'])
	sprint_id = (request.form['sprint_id']).lower()

	#get the correct sprint id if one of the options is specified
	if sprint_id == 'backlog':
		sprint_id = None
	elif sprint_id == 'current':
		sprint = Sprints.get_current_sprint(board_id)
		if sprint is not None:
			sprint_id = sprint.id

	result = Stories.create(name, description, estimate, board_id, sprint_id)

	if type(result) != dict:
		return '{"status": "success"}'
	else:
		return json.dumps(result)

@stories.route('/stories/<story_id>', methods=['DELETE'])
@Auth.authorized(Auth.STORY_AUTHORIZATION, Auth.MALFORMED_UUID_JSON)
def delete(story_id):
	'''
	Delete the given story
		arg: story_id - the id of the story to delete
	'''
	Stories.delete(story_id)

	return '{"status": "success"}'