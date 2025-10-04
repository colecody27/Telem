from flask import Flask

app = Flask(__name__)

# POST 
@app.route('/api/sensors/<id>/data', methods=['POST'])
def create_sensor(id=None):
    pass

# TODO Add query params 
# GET
@app.route('/api/sensors/<id>/data&')
def get_sensors():
    pass

# GET
@app.route('/api/sensors/<id>/data/latest')
def get_sensor(id=None):
    pass

# DELETE
@app.route('/api/sensors/<id>', methods=['DELETE'])
def remove_sensor(id=None):
    pass