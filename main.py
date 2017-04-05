import boto3
import json
import logging
import os

from command import Command
from help import Help
from rickquote import RickQuote

from base64 import b64decode
from urlparse import parse_qs

ENCRYPTED_EXPECTED_TOKEN = os.environ['kmsEncryptedToken']

kms = boto3.client('kms')
expected_token = kms.decrypt(CiphertextBlob=b64decode(ENCRYPTED_EXPECTED_TOKEN))['Plaintext']

s3 = boto3.resource('s3')
bucket = s3.Bucket('calibot-data')

logger = logging.getLogger()
logger.setLevel(logging.INFO)   

def lambda_handler(event, context):
    params = parse_qs(event['body'])
    token = params['token'][0]
    
    if token != expected_token:
        logger.error("Request token (%s) does not match expected", token)
        return respond(Exception('Invalid request token'))
   	    
   	config = None
   	
    for sub_class in Command.__subclasses__():
        if (params['text'][0] == sub_class.__name__.lower()):
            slackResponse = sub_class(None, logger).check_command(bucket)
            
    print slackResponse
    return slackResponse

