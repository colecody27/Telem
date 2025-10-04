import sqlalchemy
from flask import Flask

db = sqlalchemy()
app = Flask(__name__)
