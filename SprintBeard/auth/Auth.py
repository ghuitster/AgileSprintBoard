from flask import redirect, render_template, session, url_for

'''
This module provides decorator functions that enforce authentication. To use these functions, import the module, and then use the decorator above the
method which handles the request. The authentication decorator MUST come after any other decorators for this to work. Ex:

	@users.route('/users/<user_id>', methods=['GET'])
	@Auth.authenticated
	def view(user_id):

The above code will require that a user is logged into the site to access the page at /users/<user_id>.
'''

def authenticated(handler):
	'''
	A function decorator which requires that a user is authenticated before granting access to a handler.
		arg: handler - a function which handles a request

		return: the handler augmented such that it requires authentication
	'''
	def do_auth(*args, **kwargs):			
		if 'user' not in session:
			return redirect(url_for('login'))
		else:
			return handler(*args, **kwargs)

	return do_auth

def authorized(handler):
	'''
	A function decorator which requires that a user is authenticated, and that the user id passed in matches the authenticated user's id.
		arg: handler - a function which handles a request. Must take 'user_id' as the first argument to the function.

		return: the handler augmented such that it requires authentication
	'''
	def do_authorized(*args, **kwargs):
		if 'user' not in session:
			return redirect(url_for('login'))
			
		#make sure the userids match
		if session['user'].id == kwargs['user_id']:
			return handler(*args, **kwargs)
		else:
			return render_template('auth/unauthorized.html')

	return do_authorized
