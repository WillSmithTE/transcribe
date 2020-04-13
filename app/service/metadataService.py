from flask import Blueprint, jsonify, request, Response
from app.service.security import checkValid
from google.cloud import storage
import datetime
import json
from app.service.gcloud import getFileExtension
import os

REFRESH_PERIOD_SECONDS = 43200

def dataExpired(updatedAt):
    now = datetime.datetime.now().timestamp()
    return now - updatedAt > 43200

def getJobs():
    with open('../data.json', 'r') as file:
        data = json.load(file)
        if dataExpired(data['updatedAt']):
            file.close()
            storage_client = storage.Client()
            blobs = storage_client.list_blobs(
                'transcriptions_willsmithte',
                prefix='jobs'
            )
            jobs = []
            for blob in blobs:
                if getFileExtension(blob.name) == 'json':
                    blob.download_to_filename(blob.name)
                    with open(blob.name, 'r') as jsonFile:
                        jobs.append(json.load(jsonFile))
                        jsonFile.close()
                    os.remove(blob.name)
            with open('../data.json', 'a+') as jsonFile:
                existingData = json.load(jsonFile)
                existingData['jobs'] = jobs
                existingData['updatedAt'] = datetime.datetime.now().timestamp
                json.dump(existingData, jsonFile)
                return jsonify(jobs)
        else:
            file.close()
            return jsonify(data['jobs'])

def getDownloadUrlsForJob(id):
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
