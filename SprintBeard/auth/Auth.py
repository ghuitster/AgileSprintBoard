from flask import redirect, render_template, request, session, url_for
from models import AccessRules, Boards, Invitations
from functools import wraps

'''
This module provides decorator functions that enforce authentication. To use these functions,
import the module, and then use the decorator above the method which handles the request. The
authentication decorator MUST come after any other decorators for this to work. Ex:

	@users.route('/users/<user_id>', methods=['GET'])
	@Auth.authenticated
	def view(user_id):

The above code will require that a user is logged into the site to access the page at
/users/<user_id>.
'''

USER_AUTHORIZATION = 0
BOARD_AUTHORIZATION = 1
INVITATION_AUTHORIZATION = 2

def authenticated(handler):
	'''
	A function decorator which requires that a user is authenticated before granting access to a
	handler.
		arg: handler - a function which handles a request

		return: the handler augmented such that it requires authentication
	'''
	@wraps(handler)
	def do_auth(*args, **kwargs):			
		if 'user' not in session:
			return redirect(url_for('login', next=request.url))
		else:
			return handler(*args, **kwargs)

	return do_auth

def authorized(resource_type):
	'''
	A function decorator which requires that a user is authenticated, and that the user id passed
	in matches the authenticated user's id.
		arg: resource_type - a constant which determines which type of resource the user is trying 
		to access

		return: the handler augmented such that it requires authentication

		IMPORTANT:
			The function decorated by this decorator must have the id of the resource to be authorized
			as one of its arguments. The following are the mappings of authorization types to the name
			of the argument.

				USER_AUTHORIZATION => user_id
				BOARD_AUTHORIZATION => board_id
				INVITATION_AUTHORIZATION => invite_id
	'''
	def actual(handler):
		@wraps(handler)
		def do_authorized(*args, **kwargs):
			if 'user' not in session:
				return redirect(url_for('login', next=request.url))
			
			#get the userid of the user who owns the resource
			user_id = None
			if resource_type == USER_AUTHORIZATION:
				user_id = kwargs['user_id']
			elif resource_type == BOARD_AUTHORIZATION:
				rules = AccessRules.get_by_board(kwargs['board_id'])
				
				for rule in rules:
					if rule.user_id == session['user'].id:
						user_id = rule.user_id
			elif resource_type == INVITATION_AUTHORIZATION:
				invite = Invitations.get(kwargs['invite_id'])
				user_id = invite.user_id

			#make sure the userids match
			if user_id is not None and session['user'].id == user_id:
				return handler(*args, **kwargs)
			else:
				return render_template('auth/unauthorized.html')

		return do_authorized
	return actual
