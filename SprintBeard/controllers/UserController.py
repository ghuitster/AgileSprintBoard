from auth import Auth
from custom_render.CustomRender import render_view
from flask import Blueprint, request, session
from models import Users

users = Blueprint('users', __name__)

@users.route('/users/<user_id>', methods=['GET'])
@Auth.authorized(Auth.USER_AUTHORIZATION)
def view(user_id):
	user = Users.get(user_id)
	return render_view('users/view.html', user=user)

@users.route('/users/<user_id>/settings', methods=['POST'])
@Auth.authorized(Auth.USER_AUTHORIZATION)
def settings(user_id):
	name = request.form['name']
	email = request.form['email']
	Users.update(user_id, name, email)
	session['user'] = Users.get(user_id)
	return '{"status":"success"}'