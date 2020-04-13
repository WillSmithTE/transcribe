import urllib.request
import urllib.parse
import hashlib
from google.cloud import storage
from google.cloud import speech_v1
from google.cloud.speech import enums
import logging
import os
from pydub import AudioSegment
from pydub.utils import make_chunks
import random
import string

def getFileExtension(fileName):
    return os.path.splitext(fileName)[1][1:]

def getFileName(fileName):
    return os.path.splitext(fileName)[0]

def download(url, newFileName, oldExtension):
    logging.info('Downloading')
    tempFileName =  getFileName(newFileName) + '.' + oldExtension
    urllib.request.urlretrieve(url, tempFileName)
    AudioSegment.from_file(tempFileName, format=oldExtension).set_channels(1).export(newFileName, format = 'flac')
    os.remove(tempFileName)

def upload(filename):
    logging.info('Uploading')
    storage_client = storage.Client()
    bucket = storage_client.bucket('transcriptions_willsmithte')
    blob = bucket.blob(filename)
    blob.upload_from_filename(filename)
    os.remove(filename)

def generateTranscript(url):
    client = speech_v1.SpeechClient()
    config = {
        'language_code': 'en-IN',
        'enable_automatic_punctuation': True,
        'encoding': enums.RecognitionConfig.AudioEncoding.FLAC
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
    fileName = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10)) + '.flac'
    download(url, fileName, getFileExtension(url))
    transcription = ''
    audioFile = AudioSegment.from_file(fileName)
    audioChunks = make_chunks(audioFile, 60000)
    for i, chunk in enumerate(audioChunks):
        chunkName = str(i) + '-' + fileName
        chunk.export(chunkName, format='flac')
        upload(chunkName)
        transcription += generateTranscript('gs://transcriptions_willsmithte/' + chunkName)
    os.remove(fileName)
    return transcription

def transcribeLocal(fileName):
    upload(fileName)
    return generateTranscript('gs://transciptions_willsmithte/' + fileName)
