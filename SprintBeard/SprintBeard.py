from flask import flash, Flask, render_template
from controllers.UserController import users

app = Flask(__name__)
app.register_blueprint(users)
app.secret_key = 'some_secret'

@app.route('/')
def index():
	return render_template('index.html')

if __name__ == '__main__':
	app.debug = True
	app.run()
