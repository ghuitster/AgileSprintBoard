from auth import Auth
from flask import Blueprint, render_template, request
from models import Sprints, Stories

stories = Blueprint('stories', __name__)

@stories.route('/boards/<board_id>/stories', methods=['POST'])
@Auth.authorized(Auth.BOARD_AUTHORIZATION)
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
	sprint_id = request.form['sprint_id']

	#get the correct sprint id if one of the options is specified
	if sprint_id == 'backlog':
		sprint_id = None
	elif sprint_id == 'current':
		sprint = Sprints.get_current_sprint(board_id)
		if sprint is not None:
			sprint_id = sprint.id

	Stories.create(name, description, estimate, board_id, sprint_id)

	return '{"status": "success"}'