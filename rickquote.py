import random

from command import Command

class RickQuote(Command):
    def check_command(self, bucket):
       	for obj in bucket.objects.all():
       	    if obj.key == 'rickquotes.txt':
                lines = obj.get()['Body'].read()

        quote = random.choice(lines.splitlines())
        return { "text": "Rick says:", "response_type": "in_channel",  "attachments": [  { "text": quote }]}