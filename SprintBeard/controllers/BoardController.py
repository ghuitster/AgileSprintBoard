from flask import Blueprint, render_template
from models import Users
from uuid import UUID

boards = Blueprint('boards', __name__)

#@boards.route('/user/<user_id>/boards', methods=['GET'])
@boards.route('/user/boards', methods=['GET'])

#def view(user_id):
#	user = Users.get(UUID(user_id))
#	return render_template('boards/dashboard.html', user=user)

def view():
	return render_template('boards/dashboard.html', user='Beard')
