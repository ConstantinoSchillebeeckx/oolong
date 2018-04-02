from django.core.management.base import BaseCommand, CommandError
import os

class Command(BaseCommand):
    help = 'Pull heroku DB to local.'

    def handle(self, *args, **options):

        app = 'oolong-app'
        db = 'oolong'
        os.system('dropdb oolong')
        os.system('heroku pg:pull DATABASE_URL %s --app %s' %(db, app))

        self.stdout.write(self.style.SUCCESS('Successfully pulled heroku DB.'))
