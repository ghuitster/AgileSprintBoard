from flask import Blueprint, render_template, session, redirect
from models import Users
from uuid import UUID
from auth import Auth

boards = Blueprint('boards', __name__)

@boards.route('/dashboard', methods=['GET'])
@Auth.authorized(Auth.USER_AUTHORIZATION)
def dash():
	user_id = session['user'].id	
	return redirect('/user/%s/boards' % user_id)

@boards.route('/user/<user_id>/boards', methods=['GET'])
@Auth.authorized(Auth.USER_AUTHORIZATION)
def view(user_id):
	user = Users.get(UUID(user_id))
	boardList = Boards.getUserBoards(user_id)
	return render_template('boards/dashboard.html', user=user, boardList=boardList)

'''@boards.route('user/<user_id>/boards/#create', method=['POST'])
@Auth.authorized(Auth.USER_AUTHORIZATION)
def create(user_id):
	user = Users.get(UUID(user_id))
	Boards.createBoard(user_id)
	return render_template('boards/dashboard.html', user=user, boardList=boardList)'''