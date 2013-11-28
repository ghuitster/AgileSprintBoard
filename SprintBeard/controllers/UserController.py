from auth import Auth
from flask import Blueprint, render_template
from models import Users
from uuid import UUID

users = Blueprint('users', __name__)

@users.route('/users/<user_id>', methods=['GET'])
@Auth.authorized
def view(user_id):
	user = Users.get(UUID(user_id))
	return render_template('users/view.html', user=user)
