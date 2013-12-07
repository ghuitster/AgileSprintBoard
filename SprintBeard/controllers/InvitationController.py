from auth import Auth
from flask import Blueprint, request
from custom_render.CustomRender import render_view
from models import Invitations

invitations = Blueprint('invitations', __name__)

@invitations.route('/boards/<board_id>/invite', methods=['POST'])
@Auth.authorized(Auth.BOARD_AUTHORIZATION)
def invite(board_id):
	'''
	Invite a user to use a board with the given privileges
		arg: board_id - the board for which to generate an invite
		arg: privileges - the privileges to give the user. Use the constants in Boards
		arg: other - the id of the user to invite
	'''
	other_email = request.form['email']
	privileges = int(request.form['privileges'])
	Invitations.invite(other_email, board_id, privileges)
	return '{"status": "success"}'

@invitations.route('/invitations/<invite_id>/accept', methods=['POST'])
@Auth.authorized(Auth.INVITATION_AUTHORIZATION)
def accept(invite_id):
	'''
	Accept an invitation to collaborate on a board
	arg: invite_id - the id of the invitation
	'''
	Invitations.respond_to_invite(invite_id, True)
	return '{"status":"success"}'

@invitations.route('/invitations/<invite_id>/reject', methods=['POST'])
@Auth.authorized(Auth.INVITATION_AUTHORIZATION)
def reject(invite_id):
	'''
	Reject an invitation to collaborate on a board
	arg: invite_id - the id of the invitation
	'''
	Invitations.respond_to_invite(invite_id, False)
	return '{"status": "success"}'
