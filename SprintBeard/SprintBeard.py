from flask import flash, Flask, render_template, redirect, session, url_for
from controllers.BoardController import boards
from controllers.InvitationController import invitations
from controllers.UserController import users
from flask.ext.openid import OpenID
from models import Users

app = Flask(__name__)
app.secret_key = 'some_secret'
oid = OpenID(app)
app.register_blueprint(boards)
#app.register_blueprint(invitations)
app.register_blueprint(users)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/login')
@oid.loginhandler
def login():
	'''
	Log the user into the SprintBeard application. Results in the user being redirected to the Google OpenID process.
	'''
	#if we've already logged in, just redirect to the selected url	

	if 'openid' in session and 'user' not in session:
		session['user'] = Users.get_by_openid(session['openid'])
		return redirect(oid.get_next_url())
	else:
		return oid.try_login("https://www.google.com/accounts/o8/id",ask_for=['email', 'fullname'])

@oid.after_login
def new_user(resp):
	'''
	Creates a new user if the user had not previously signed in with openid. Otherwise, just sets the session to the correct user.
		arg: resp - the response from the openid provider

		return: the view to display (redirected to originally asked for page)
	'''
	session['openid'] = resp.identity_url
	user = Users.get_by_openid(session['openid'])
	#if we haven't created the user before, create it
	if user is None:
		user = Users.create(resp.fullname, resp.email)
		Users.create_openid_association(user.id, session['openid'])
		session['user'] = user
	else:
		session['user'] = user

	return redirect(oid.get_next_url())

@app.route('/logout')
def logout():
	'''
	Logout the user from the service. Ends the session
	'''
	session.pop('openid', None)
	session.pop('user', None)
	return redirect(oid.get_next_url())

if __name__ == '__main__':
	app.debug = True
	app.run()

