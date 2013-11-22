from flask import Blueprint, render_template

users = Blueprint('users', __name__)

@users.route('/users/<user_id>', methods=['GET'])
def view(user_id):
	return render_template('users/view.html', user_id=user_id)