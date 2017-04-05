from command import Command

class Help(Command):
    def check_command(self, bucket):
        for obj in bucket.objects.all():
            if obj.key == 'help.txt':
                helpText = obj.get()['Body'].read()

        return { "text": "How to use /calibot", "attachments": [ {"text": helpText }]}
