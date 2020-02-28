from flask import Flask
from .views import RunnerAPI

app = Flask(__name__)

app.add_url_rule("/run", view_func=RunnerAPI.as_view("run"))
