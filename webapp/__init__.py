import os
from flask import Flask


app = Flask(__name__)
import webapp.views

path = os.path.dirname(os.path.abspath(__file__))

config_file = os.path.join(path, '../config.cfg')
app.config.from_pyfile(config_file)

app.config['HOSTNAME'] = os.uname()[1]
app.config['APPNAME'] = 'Micro Services Testing'
#app.config['API_URI'] = os.environ['API_URL']

path = os.path.dirname(os.path.abspath(__file__))
'''Read the secret key from file is it exist or generate
   a secret random key for the session and write in the file'''
secret_file = os.path.join(path, '../secret.key')
if os.path.isfile(secret_file):
    with open(secret_file, 'r') as fh:
        app.secret_key = fh.read()
else:
    app.secret_key = os.urandom(128)
    with open(secret_file, 'w') as fh:
        fh.write(app.secret_key)
