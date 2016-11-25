from flask import Flask, redirect, url_for, session, request, jsonify
from flask import render_template
from flask_oauthlib.client import OAuth



app = Flask(__name__)
app.debug = True
app.secret_key = 'development'

oauth = OAuth(app)

github = oauth.remote_app(
    'github',
    consumer_key='9668bff6a6d0cf60d387',
    consumer_secret='1adfdb0718d49e1f33bb68376ef439658c5f947d',
    request_token_params={'scope': 'user:email'},
    base_url='https://api.github.com/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize'
)

@app.route('/')
@app.route('/index')

def index():
    # user = {'nickname': 'Miguel'}  # fake user
    return render_template('index.html',
                           title='Home')


# @app.route('/oauth')

# def loginWithGithub():
# 	if 'github_token' in session:
# 		me = github.get('user')
# 		return jsonify(me.data)
# 	return redirect(url_for('login'))

@app.route('/login')
def login():
    print("inside login")
    print(url_for('authorized', _external=True))
    print("printed URL")
    return github.authorize(callback=url_for('authorized', _external=True))

@app.route('/logout')
def logout():
    session.pop('github_token', None)
    return redirect(url_for('index'))

@app.route('/login/authorized')
def authorized():
    print("inside authorized")
    resp = github.authorized_response()
    if resp is None or resp.get('access_token') is None:
        return 'Access denied: reason=%s error=%s resp=%s' % (
            request.args['error'],
            request.args['error_description'],
            resp
        )
    session['github_token'] = (resp['access_token'], '')
    me = github.get('user')
    return jsonify(me.data)
    #return redirect(url_for('index'))


@github.tokengetter
def get_github_oauth_token():
    return session.get('github_token')

if __name__ == "__main__":
	app.run()