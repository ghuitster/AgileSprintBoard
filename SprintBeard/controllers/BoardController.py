from auth import Auth
from custom_render.CustomRender import render_view
from flask import Blueprint, render_template, request, session, redirect
from models import Boards, Invitations, Users
from uuid import UUID

boards = Blueprint('boards', __name__)

@boards.route('/dashboard', methods=['GET'])
@Auth.authenticated
def dash():
	'''
		Primary purpose is to act as the Authetication before redirecting to the Dashboard.
		return: redirect
	'''
	user_id = session['user'].id
	return redirect('/user/%s/boards' % user_id)

@boards.route('/user/<user_id>/boards', methods=['GET'])
@Auth.authorized(Auth.USER_AUTHORIZATION, Auth.MALFORMED_UUID_HTML)
def view_for_user(user_id):
	'''
		Generates the Board and Invite information for the Board Dashboard.
		arg: user_id - The User who's Dashboard will be rendered.
		return: render_view
	'''
	user = Users.get(user_id)
	board_List = Boards.get_user_boards(user_id)
	invite_list = Invitations.get_by_user(user_id)
	return render_view('boards/dashboard.html', board_List=board_List, invite_list=invite_list)

@boards.route('/user/<user_id>/boards', methods=['POST'])
@Auth.authorized(Auth.USER_AUTHORIZATION, Auth.MALFORMED_UUID_JSON)
def create(user_id):
	'''
		Create a Board.
		arg: user_id - The User who created the board.
		return: JSON status
	'''
	name = request.form['name']
	Boards.create(user_id, name)
	return '{"status":"success"}'

@boards.route('/boards/<board_id>', methods=['GET'])
@Auth.authorized(Auth.BOARD_AUTHORIZATION, Auth.MALFORMED_UUID_HTML)
def view(board_id):
	'''
		Get a view of the requested board.
		arg: board_id - The board to view.
		return: render_view
	'''
	board = Boards.view(board_id)
	return render_view('boards/view.html', board=board)

@boards.route('/boards/<board_id>', methods=['DELETE'])
@Auth.authorized(Auth.BOARD_AUTHORIZATION, Auth.MALFORMED_UUID_JSON)
def delete(board_id):
	'''
		Delete a Board.
		arg: board_id - The board to be deleted.
		return: JSON status
	'''
	Boards.delete(board_id)
	return '{"status":"success"}'






