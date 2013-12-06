from auth import Auth
from custom_render.CustomRender import render_view
from flask import Blueprint
from models import Users

users = Blueprint('users', __name__)

@users.route('/users/<user_id>', methods=['GET'])
@Auth.authorized(Auth.USER_AUTHORIZATION)
def view(user_id):
	user = Users.get(user_id)
	return render_view('users/view.html', user=user)

@users.route('/users/<user_id>/settings', methods=['GET'])
@Auth.authorized(Auth.USER_AUTHORIZATION)
def settings(user_id):
	user = Users.get(user_id)
	return render_view('users/settings.html', user=user)
