from flask import Flask

app = Flask(__name__)

# POST 
@app.route('/api/sensors', methods=['POST'])
def create_sensor():
    pass

# GET
@app.route('/api/sensors')
def get_sensors():
    pass

# GET
@app.route('/api/sensors/<id>')
def get_sensor(id=None):
    pass

# PUT
@app.route('/api/sensors/<id>', methods=['PUT'])
def update_sensor(id=None):
    pass

# DELETE
@app.route('/api/sensors/<id>', methods=['DELETE'])
def remove_sensor(id=None):
    pass