from django.core.management.base import BaseCommand, CommandError
import os

class Command(BaseCommand):
    help = 'Push local DB to heroku.'

    def handle(self, *args, **options):

        app = 'oolong-app'
        os.system('heroku pg:reset --app %s --confirm %s' %(app, app))
        os.system('heroku pg:push oolong DATABASE_URL --app %s' %app)

        self.stdout.write(self.style.SUCCESS('Successfully pushed DB to heroku.'))
