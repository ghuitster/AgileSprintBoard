from auth import Auth
from custom_render.CustomRender import render_view
from flask import Blueprint, request
import json
from models import AccessRules

access_rules = Blueprint('access_rules', __name__)

@access_rules.route('/boards/<board_id>/access_rules', methods=['POST'])
@Auth.authorized(Auth.BOARD_AUTHORIZATION, Auth.MALFORMED_UUID_JSON)
def create(board_id):
	'''
	Create a new access rule to a board. 
		arg: board_id - the id of the board to add a rule for
		POST arg: user_id - the id of the user to add a rule for
		POST arg: privileges - the privilege level to give the user
	'''

	user_id = request.form['user_id']
	privileges = int(request.form['privileges'])
	result = AccessRules.create(use_id, board_id, privileges)

	if type(result) != dict:
		return '{"status": "success"}'
	else:
		return json.dumps(result)

@access_rules.route('/boards/<board_id>/access_rules/<user_id>', methods=['DELETE'])
@Auth.authorized(Auth.BOARD_AUTHORIZATION, Auth.MALFORMED_UUID_JSON)
def delete(board_id, user_id):
	'''
	Delete a user's rights to access a board.
		arg: board_id - the id of the board the user had access to
		arg: user_id - the id of the user from whom to remove access
	'''
	result = AccessRules.delete(board_id, user_id)

	if type(result) != dict:
		return '{"status": "success"}'
	else:
		return json.dumps(result)
