from flask import Blueprint, jsonify, request, Response
from security import checkValid
from google.cloud import storage
import datetime

metadata_api = Blueprint('metadata_api', __name__)

@metadata_api.route('/metadata', methods=['GET'])
def getAll():
    return jsonify([
        {
            'id': 'KJHG1019KS',
            'excerptLink': 'placeholderlink',
            'length': 500,
            'inProgress': False,
            'language': 'en-US',
            'cost': 5.60,
            'deadline': 8503209
        }
    ])


@metadata_api.route('/metadata/<id>', methods=['GET'])
def getTranscriptionData(id):
    return jsonify({
        'id': 'KJHG1019KS',
        'excerptLink': 'placeholderlink',
        'length': 500,
        'inProgress': False,
        'language': 'en-US',
        'cost': 5.60,
        'deadline': 8503209,
        'description': 'this is a really long text which does not pay great :)'
    })

@metadata_api.route('/metadata/download/<id>', methods=['GET'])
def download(id):
    checkValid(request.headers.get('Authorization'))
    storage_client = storage.Client()
    bucket = storage_client.bucket('transcriptions_willsmithte')
    audioBlob = bucket.blob('jobs/' + id + '/audio.flac')
    textBlob = bucket.blob('jobs/' + id + '/transcription.txt')
    audioUrl = audioBlob.generate_signed_url(
        version='v4',
        expiration=datetime.timedelta(minutes=15),
        method='GET'
    )
    textUrl = textBlob.generate_signed_url(
        version='v4',
        expiration=datetime.timedelta(minutes=15),
        method='GET'
    )
    return jsonify({
        'audio': audioUrl,
        'transcription': textUrl
    })
    
@metadata_api.route('/metadata/apply/<id>', methods=['GET'])
def apply(id):
    checkValid(request.headers.get('Authorization'))
    return jsonify('passed')