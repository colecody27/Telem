from flask import Flask

app = Flask(__name__)

# GET
@app.route('/api/auth/me')
def get_user():
    pass

# POST
@app.route('/api/auth/login')
def login():
    pass

# POST
@app.route('/api/auth/register')
def register():
    pass