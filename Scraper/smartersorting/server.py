import os
from werkzeug.utils import secure_filename
from functools import wraps
from flask import Flask, render_template, request, url_for, Response, redirect


UPLOAD_FOLDER = '/root/pythonServer/uploaded'
ALLOWED_EXTENSIONS = set(['json', 'txt'])

# authentication functions
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

# create a new web app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# allowed file name
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# home page
@app.route('/', methods=['GET', 'POST'])
@requires_auth
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect("/hello")
    return render_template('index.html')

@app.route('/hello', methods=['GET', 'POST'])
@requires_auth
def timestamps():
    fileRead = open("/root/pythonServer/uploaded/timestamps.txt", "r+")
    fill_file = fileRead.read()
    fileRead.close()
    lines = fill_file.split("\n")

    element = []

    for line in lines:
        timestamps_elements = line.split(",");
        try:
            elementos = []
            elementos.append(timestamps_elements[0])
            elementos.append(timestamps_elements[1])
            element.append(elementos)
        except:
            pass
    return render_template('timestamp.html', elements=element)

# Run the app :)
if __name__ == '__main__':
  app.run()