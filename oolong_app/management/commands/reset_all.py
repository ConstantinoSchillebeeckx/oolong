from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
import os

class Command(BaseCommand):
    help = 'Drop/re-create DB, rerun all migrations, migrate, load init data.'

    def handle(self, *args, **options):

        db = 'oolong'
        app = 'oolong_app'

        # reset DB
        os.system('dropdb %s' %db)
        os.system('createdb %s' %db)

        # redo migrations
        os.system('rm %s/migrations/000*py' %app)
        call_command('makemigrations')
        call_command('migrate')

        # fill DB
        os.system('psql -d %s -a -f %s/db_init.sql;' %(db, app))

        self.stdout.write(self.style.SUCCESS('Successfully reset everything.'))
