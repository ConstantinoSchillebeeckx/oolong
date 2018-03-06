# middleware.py

from django.utils import timezone

import pytz


class TimezoneMiddleware(object):

    def process_request(self, request):

        # will want to have the local timezone
        # to be loaded from user data instead

        if request.user.is_authenticated():
            timezone.activate(pytz.timezone('America/Chicago'))
        else:
            timezone.deactivate()
