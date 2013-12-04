from auth import Auth
from flask import Blueprint, render_template
from models import Users

users = Blueprint('users', __name__)

@users.route('/users/<user_id>', methods=['GET'])
@Auth.authorized(Auth.USER_AUTHORIZATION)
def view(user_id):
	user = Users.get(user_id)
	return render_template('users/view.html', user=user)

@users.route('/users/<user_id>/settings', methods=['GET'])
@Auth.authorized(Auth.USER_AUTHORIZATION)
def settings(user_id):
	user = Users.get(user_id)
	return render_template('users/settings.html', user=user)
