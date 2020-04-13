from flask import Flask, jsonify
from flask_cors import CORS
import os
from security import Forbidden
from api.metadata import metadata_api
from api.transcribe import transcribe_api
from api.security import security_api

app = Flask(__name__)
CORS(app)

app.register_blueprint(metadata_api)
app.register_blueprint(transcribe_api)
app.register_blueprint(security_api)

@app.errorhandler(Forbidden)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=os.environ.get('PORT', '5000'))
