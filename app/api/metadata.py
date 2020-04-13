from flask import Blueprint, jsonify, request, Response
from app.service.security import checkValid
from google.cloud import storage
import datetime
import json
from app.service.gcloud import getFileExtension
import os
from app.service.metadataService import getJobs, getDownloadUrlsForJob

metadata_api = Blueprint('metadata_api', __name__)

@metadata_api.route('/metadata', methods=['GET'])
def getAll():
    return getJobs()

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
def getDownloadLinks(id):
    return getDownloadUrlsForJob(id)

@metadata_api.route('/metadata/apply/<id>', methods=['GET'])
def apply(id):
    checkValid(request.headers.get('Authorization'))
    return jsonify('passed')