from functools import wraps
from flask import Flask, render_template, request, url_for, Response

def check_auth(username, password):
    return username == 'admin' and password == 'secret'


def authenticate_failed():
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials\n\nThe authentication header is in ["WWW-Authenticate"]', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate_failed()
        return f(*args, **kwargs)
    return decorated

app = Flask(__name__)

@app.route('/emails/')
@requires_auth
def hello():
    return render_template('index.html')

# Run the app :)
if __name__ == '__main__':
  app.run()