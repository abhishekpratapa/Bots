from functools import wraps
from flask import Flask, render_template, request, url_for, Response

####################   TEST APP ###########################

app = Flask(__name__)

# modular app recode

def check_auth(username, password):
    return username == 'admin' and password == 'secret'


def authenticate_failed():
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials\n\nThe authentication header is in ["WWW-Authenticate"]', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def help_authenticate():
    return Response(
        'Congratulations you have authenticated.\n'
        'Here are the header calls\n\n ["get-info"] ["post-info"]', 201,
        {'get-info': '{"type":"[email_scraped] [google_search] [linkein_people]" REQUIRED PARAMETERS FOR EMAILhello}', 'post-info': ''})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate_failed()
        return f(*args, **kwargs)
    return decorated

# modular app recode

# define a start page for the Cannibis page
@app.route('/')
@requires_auth
def form():
    return help_authenticate()
    #return render_template('index.html')


# return Json String
@app.route('/hello/')
@requires_auth
def hello():
    name = None
    email = None

    try:
        name=request.form['sent_Post']
        email=request.form['second_post']
    except:
        pass
    if not name:
        print("hello")
    return help_authenticate()
    #return render_template('form_action.html', name=name, email=email)


# Run the app :)
if __name__ == '__main__':
  app.run()