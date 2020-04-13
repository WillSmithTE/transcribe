from flask import jsonify

# willyschnite

VALID_TOKENS = [
    'e4ee684fd1129640d1942c990ee91062e054ecf5042f3f293305942d7a51ebb0'
]

def isValid(token):
    return token in VALID_TOKENS

def checkValid(token):
    if not isValid(token):
        raise Forbidden('Invalid security token')

class Forbidden(Exception):
    status_code = 403

    def __init__(self, message, payload=None):
        Exception.__init__(self)
        self.message = message
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv
