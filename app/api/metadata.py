from flask import Blueprint, jsonify, request, Response
from app.service.security import checkValid
from google.cloud import storage
import datetime
import json
from app.service.gcloud import getFileExtension
import os
from app.service.metadataService import getJobs, getDownloadUrlsForJob, getJobData

metadata_api = Blueprint('metadata_api', __name__)

@metadata_api.route('/metadata', methods=['GET'])
def getAll():
    return getJobs()

@metadata_api.route('/metadata/<id>', methods=['GET'])
def getTranscriptionData(id):
    return getJobData(id)

@metadata_api.route('/metadata/download/<id>', methods=['GET'])
def getDownloadLinks(id):
    return getDownloadUrlsForJob(id)

@metadata_api.route('/metadata/apply/<id>', methods=['GET'])
def apply(id):
    checkValid(request.headers.get('Authorization'))
    return jsonify('passed')