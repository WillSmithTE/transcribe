import urllib.request
import hashlib
from google.cloud import storage
from google.cloud import speech_v1
import logging

def download(url, savePath):
    logging.info('Downloading')
    urllib.request.urlretrieve(url, savePath)

def upload(savePath, filename):
    logging.info('Uploading')
    storage_client = storage.Client()
    bucket = storage_client.bucket('transcriptions_willsmithte')
    blob = bucket.blob(filename)
    blob.upload_from_filename(savePath)

def generateTranscript(url):
    client = speech_v1.SpeechClient()
    config = {
        'sample_rate_hertz': 16000,
        'language_code': 'en-US'
    }
    audio = { 'uri': url }
    logging.info('Generating transcript')
    operation = client.long_running_recognize(config, audio)
    response = operation.result()
    toReturn = ''
    for result in response.results:
        toReturn += result.alternatives[0].transcript + ' '
    return toReturn

def saveTranscript(transcript, fileName):
    with open(fileName, 'w') as text_file:
        text_file.write(transcript)

def main(url):
    fileName = hashlib.sha256(bytes(url, encoding='utf-8')).hexdigest()
    download(url, fileName)
    upload(fileName, fileName)
    return generateTranscript('gs://transcriptions_willsmithte/' + fileName)

