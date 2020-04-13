from flask import Blueprint, jsonify, request
from security import Forbidden, isValid

security_api = Blueprint('security_api', __name__)

@security_api.route('/valid', methods=['GET'])
def isValidApi():
    return jsonify(isValid(request.args.get('token')))
