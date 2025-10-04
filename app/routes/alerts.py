from flask import Flask

app = Flask(__name__)

# GET
@app.route('/api/alerts')
def get_alerts():
    pass

# GET
@app.route('/api/alerts/<id>/')
def get_alert(id=None):
    pass

# PUT
@app.route('/api/alerts/<id>/ack')
def ack_alert(id=None):
    pass