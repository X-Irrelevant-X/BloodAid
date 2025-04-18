from flask import Flask
from views import home

app = Flask(__name__)

# Home page
app.add_url_rule('/', view_func=home, endpoint='home')