from flask import Blueprint, request, render_template
from models import Invitations

invitations = Blueprint('invitations', __name__)

@invitations.route('/boards/<board_id>/invite', methods=['POST'])
def invite(board_id):
	'''
	Invite a user to use a board with the given privileges
		arg: board_id - the board for which to generate an invite
		arg: privileges - the privileges to give the user. Use the constants in Boards
		arg: other - the id of the user to invite
	'''
	other_id = request.form['other_id']
	privileges = int(request.form['privileges'])
	Invitations.invite(other_id, board_id, privileges)
	return render_template('boards/dashboard.html', user='Beard')

@invitations.route('/invitations/<invite_id>/accept', methods=['POST'])
def accept(invite_id):
	'''
	Accept an invitation to collaborate on a board
	arg: invite_id - the id of the invitation
	'''
	Invitations.respond_to_invite(invite_id, True)
	return "done"

@invitations.route('/invitations/<invite_id>/reject', methods=['POST'])
def accept(invite_id):
	'''
	Reject an invitation to collaborate on a board
	arg: invite_id - the id of the invitation
	'''
	Invitations.respond_to_invite(invite_id, False)
	return "done"
