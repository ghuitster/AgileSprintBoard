from auth import Auth
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
def view(user_id):
	user = Users.get(user_id)
	boardList = Boards.get_user_boards(user_id)
	return render_template('boards/dashboard.html', user=user, boardList=boardList)

@boards.route('/user/<user_id>/boards', methods=['POST'])
@Auth.authorized(Auth.USER_AUTHORIZATION)
def create_board(user_id):
	name = request.form['name']
	Boards.create_board(user_id, name)
	return '{"status":"success"}'

@boards.route('/boards/<board_id>', methods=['DELETE'])
@Auth.authorized(Auth.BOARD_AUTHORIZATION)
def delete_board(board_id):
	Boards.delete_board(board_id)
	return '{"status":"success"}'

