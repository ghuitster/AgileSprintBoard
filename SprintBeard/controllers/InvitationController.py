from auth import Auth
from custom_render.CustomRender import render_view
from flask import Blueprint, request
import json
from models import Invitations

invitations = Blueprint('invitations', __name__)

@invitations.route('/boards/<board_id>/invite', methods=['POST'])
@Auth.authorized(Auth.BOARD_AUTHORIZATION, Auth.MALFORMED_UUID_JSON)
def invite(board_id):
	'''
	Invite a user to use a board with the given privileges POST Contains email, privileges, board_id
	arg: board_id - ID of board being shared
	'''
	other_email = request.form['email']
	privileges = int(request.form['privileges'])

	Invitations.invite(other_email, board_id, privileges)

	return '{"status":"success"}'
	
@invitations.route('/invitations/<invite_id>/accept', methods=['POST'])
@Auth.authorized(Auth.INVITATION_AUTHORIZATION, Auth.MALFORMED_UUID_JSON)
def accept(invite_id):
	'''
	Accept an invitation to collaborate on a board
	arg: invite_id - the id of the invitation
	'''
	Invitations.respond_to_invite(invite_id, True)
	return '{"status":"success"}'

@invitations.route('/invitations/<invite_id>/reject', methods=['POST'])
@Auth.authorized(Auth.INVITATION_AUTHORIZATION, Auth.MALFORMED_UUID_JSON)
def reject(invite_id):
	'''
	Reject an invitation to collaborate on a board
	arg: invite_id - the id of the invitation
	'''
	Invitations.respond_to_invite(invite_id, False)
	return '{"status": "success"}'
