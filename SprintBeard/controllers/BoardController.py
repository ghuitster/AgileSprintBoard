from flask import Blueprint, render_template
from models import Users
from uuid import UUID

boards = Blueprint('boards', __name__)

@boards.route('/user/<user_id>/boards', methods=['GET'])
def view(user_id):
	user = Users.get(UUID(user_id))	# Get User from User.py
	boardList = Boards.getUserBoards(user_id)
	return render_template('boards/dashboard.html', user=user, boardList=boardList)

#@boards.route('/user/boards', methods=['GET'])
#def view():
#	return render_template('boards/dashboard.html', user='Beard')
