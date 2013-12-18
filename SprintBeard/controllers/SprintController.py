from auth import Auth
from custom_render.CustomRender import render_view
from flask import Blueprint, request
import json
from models import Sprints

sprints = Blueprint('sprints', __name__)

@sprints.route('/boards/<board_id>/sprints/<sprint_id>/dates', methods=['POST'])
@Auth.authorized(Auth.BOARD_AUTHORIZATION, Auth.MALFORMED_UUID_JSON)
def change_dates(board_id, sprint_id):
	'''
	Change the start and end date on a sprint.
		arg: board_id - the id of the board that owns the sprint
		arg: sprint_id - the id of the sprint
		POST arg: start - the start date of the sprint (MM-DD-YYYY)
		POST arg: end - the end date of the sprint (MM-DD-YYYY)
	'''
	start = request.form['start']
	end = request.form['end']

	Sprints.change_dates(sprint_id, start, end)

	return '{"status": "success"}'