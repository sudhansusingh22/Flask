from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
@app.route('/index')

def index():
    # user = {'nickname': 'Miguel'}  # fake user
    return render_template('index.html',
                           title='Home')

@app.route('/about')
def x():
	return "Hello"

if __name__ == "__main__":
	app.run()