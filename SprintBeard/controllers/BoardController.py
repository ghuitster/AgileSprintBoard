from auth import Auth
from custom_render.CustomRender import render_view
from flask import Blueprint, render_template, request, session, redirect
from models import Boards, Users
from uuid import UUID

boards = Blueprint('boards', __name__)

@boards.route('/dashboard', methods=['GET'])
@Auth.authenticated
def dash():
	user_id = session['user'].id
	return redirect('/user/%s/boards' % user_id)

@boards.route('/user/<user_id>/boards', methods=['GET'])
@Auth.authorized(Auth.USER_AUTHORIZATION)
def view_for_user(user_id):
	user = Users.get(user_id)
	boardList = Boards.get_user_boards(user_id)
	return render_view('boards/dashboard.html', boardList=boardList)

@boards.route('/user/<user_id>/boards', methods=['POST'])
@Auth.authorized(Auth.USER_AUTHORIZATION)
def create(user_id):
	name = request.form['name']
	Boards.create(user_id, name)
	return '{"status":"success"}'

@boards.route('/boards/<board_id>', methods=['GET'])
@Auth.authorized(Auth.BOARD_AUTHORIZATION)
def view(board_id):
	'''
	Get a view of the requested board.
		arg: board_id - the board to view

		return: the view
	'''
	board = Boards.view(board_id)
	return render_view('boards/view.html', board=board)

@boards.route('/boards/<board_id>', methods=['DELETE'])
@Auth.authorized(Auth.BOARD_AUTHORIZATION)
def delete(board_id):
	Boards.delete(board_id)
	return '{"status":"success"}'

