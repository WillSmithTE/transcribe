from flask import Flask
from flask import jsonify
from flask import request
from gcloud import main
import os
from security import Forbidden, isValid, checkValid

app = Flask(__name__)

@app.route('/transcribe', methods=['GET'])
def transcribe():
    checkValid('derp')
    return main(request.args.get('url'))

@app.errorhandler(Forbidden)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=os.environ.get('PORT', '5000'))
