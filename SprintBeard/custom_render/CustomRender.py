from flask import render_template, session

def render_view(filename, *args, **kwargs):
	'''
	A wrapper around Flask's render_template function. Basically does the same thing except that it
	always sends the current user in the session to the template specified by the user.
		arg: filename - the filename of the template to render
		arg: args - the list arguments that would normally go to render_template
		arg: kwargs - the dictionary arguments that would normally go to render_template

	Usage Example:

		If you were trying to render the board view, and would normally call:

			render_template('/boards/view.html', board=board_object)

		you should call this function with:

			render_view('/boards/view.html', board=board_object)

		So it's exactly the same as the normal call to render_template, but the template
		that gets rendered will also have a variable 'user' that contains the current user
		or None.
	'''

	#if the previous template is already sending a user, just send that
	if 'user' in kwargs:
		return render_template(filename, *args, **kwargs)

	user = None
	if 'user' in session:
		user = session['user']

	return render_template(filename, user=user, *args, **kwargs)