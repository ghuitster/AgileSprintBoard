from auth import Auth
from custom_render.CustomRender import render_view
from flask import Blueprint, request
from models import AccessRules

access_rules = Blueprint('access_rules', __name__)

@access_rules.route('/boards/<board_id>/access_rules', methods=['POST'])
@Auth.authorized(Auth.BOARD_AUTHORIZATION)
def create(board_id):
	'''
	Create a new access rule to a board. 
		arg: board_id - the id of the board to add a rule for
		POST arg: user_id - the id of the user to add a rule for
		POST arg: privileges - the privilege level to give the user
	'''

	user_id = request.form['user_id']
	privileges = int(request.form['privileges'])
	AccessRules.create(use_id, board_id, privileges)

	return '{"status": "success"}'
