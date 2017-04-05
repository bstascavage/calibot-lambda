import boto3
import os
import random

from base64 import b64decode

from command import Command
from twitter import *
from random import randint

class GoodNews(Command):
    def check_command(self, bucket):
        return { "text": "<%s>" % self.get_news(200), "unfurl_links": True, "unfurl_media": True, "response_type": "in_channel" }

    def get_news(self, count):
        # Decrypting Twitter keys from Lambda ENV vars
        kms = boto3.client('kms')

        ENCRYPTED_ACCESS_KEY = os.environ['twitterAccessKey']
        access_key = kms.decrypt(CiphertextBlob=b64decode(ENCRYPTED_ACCESS_KEY))['Plaintext']
        ENCRYPTED_ACCESS_SECRET = os.environ['twitterAccessSecret']
        access_secret = kms.decrypt(CiphertextBlob=b64decode(ENCRYPTED_ACCESS_SECRET))['Plaintext']
        ENCRYPTED_CONSUMER_KEY = os.environ['twitterConsumerKey']
        consumer_key = kms.decrypt(CiphertextBlob=b64decode(ENCRYPTED_CONSUMER_KEY))['Plaintext']
        ENCRYPTED_CONSUMER_SECRET = os.environ['twitterConsumerSecret']
        consumer_secret = kms.decrypt(CiphertextBlob=b64decode(ENCRYPTED_CONSUMER_SECRET))['Plaintext']
        
        twitter = Twitter(auth = OAuth(access_key, access_secret, consumer_key, consumer_secret))
        
        # Getting Godnews twitter user
        user = os.environ['goodNewsUser']

        try:
            results = twitter.statuses.user_timeline(screen_name = user, count = count)
        except Exception as e:
            self.logger.error("Could not grab Twitter timeline for user: %s" % user)
            self.logger.error(e)

        return_result = results[randint(0,count-1)]['entities']['media'][0]['expanded_url']
        return return_result
