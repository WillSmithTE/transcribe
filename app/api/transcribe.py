from flask import Blueprint, request
from app.service.gcloud import main, transcribeLocal, generateTranscript
from app.service.security import Forbidden, isValid, checkValid

transcribe_api = Blueprint('transcribe_api', __name__)

@transcribe_api.route('/transcribe', methods=['GET'])
def transcribe():
    return main(request.args.get('url'))

@transcribe_api.route('/transcribeLocal', methods=['GET'])
def transcribeLocalApi():
    return transcribeLocal(request.args.get('filename'))

@transcribe_api.route('/transcribeHosted', methods=['GET'])
def transcribeHostedApi():
    return generateTranscript('gs://transcriptions_willsmithte/' + request.args.get('url'))
