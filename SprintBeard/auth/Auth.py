from flask import redirect, render_template, request, session, url_for
from functools import wraps
from models import AccessRules, Boards, Invitations, Stories, Tasks

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
STORY_AUTHORIZATION = 3
TASK_AUTHORIZATION = 4

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
 	do_auth.__name__ = handler.__name__
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
				STORY_AUTHORIZATION => story_id
				TASK_AUTHORIZATION => task_id
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
				user_id = has_board_access(kwargs['board_id'])
			elif resource_type == INVITATION_AUTHORIZATION:
				invite = Invitations.get(kwargs['invite_id'])
				user_id = invite.user_id
			elif resource_type == STORY_AUTHORIZATION:
				story = Stories.get(kwargs['story_id'])
				if story is not None:
					user_id = has_board_access(story.board_id)
			elif resource_type == TASK_AUTHORIZATION:
				task = Tasks.get(kwargs['task_id'])
				if task is not None:
					story = Stories.get(task.story_id)
					if story is not None:
						user_id = has_board_access(story.board_id)
						
			#make sure the userids match
			if user_id is not None and session['user'].id == user_id:
				return handler(*args, **kwargs)
			else:
				return render_template('auth/unauthorized.html')
		do_authorized.__name__ = handler.__name__
		return do_authorized
	return actual

def has_board_access(board_id):
	'''
	Get the user_id of the user if the current user has access to the board.
		arg: board_id - the id of the board to look up

		return: the id of the user if found, or None if not found
	'''
	rules = AccessRules.get_by_board(board_id)

	for rule in rules:
		if rule.user_id == session['user'].id:
			return rule.user_id
