from flask import jsonify

def isValid(token):
    return True

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
