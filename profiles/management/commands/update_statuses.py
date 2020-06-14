import sys
import time
import json
from optparse import make_option

import twitter
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from profiles.models import Profile, Status

class Command(BaseCommand):
    def handle(self, *args, **options):
        self.api = self.get_api()
        for profile in Profile.objects.all():
            self.save_user_timeline(profile)

    def get_api(self):
        api = twitter.Api(consumer_key=settings.CONSUMER_KEY,
                          consumer_secret=settings.CONSUMER_SECRET,
                          access_token_key=settings.ACCESS_TOKEN_KEY,
                          access_token_secret=settings.ACCESS_TOKEN_SECRET)
        try:
            api.VerifyCredentials()
        except twitter.error.TwitterError as e:
            self.stderr.write('Twitter authentication failed.')
            sys.exit(1)
        return api

    def save_user_timeline(self, profile):
        """ takes a Profile model object, captures all the profile's statuses. """
        kwargs = {'count': 200, 'since_id': None, 'max_id': None}
        try:
            newest_status = Status.objects.filter(profile=profile).order_by('id')[0]
        except IndexError:
            pass
        else:  # don't go back beyond the newest status currently known
            kwargs['since_id'] = newest_status.status_id
            if newest_status.status_id == profile.user_json['status']['id']:
                print "nothing to do"
                return None
        print kwargs
        try:
            statuses = self.api.GetUserTimeline(profile.profile_id, **kwargs)
        except twitter.error.TwitterError as e:
            print "twitter error {} on {}".format(e, profile.screen_name)
            return None
        while len(statuses) > 0 and statuses[-1].id != kwargs['max_id']:
            time.sleep(5)  # should delay enough between queries to overcome the rate limit

            kwargs['max_id'] = statuses[-1].id - 1
            status_ids = [s.id for s in statuses]
            existing_ids = Status.objects.filter(status_id__in=status_ids)
            statuses = [s for s in statuses
                        if s.id not in existing_ids.values_list('status_id', flat=True)]

            status_objs = []
            for s in statuses:
                status_objs.append(Status(status_id=s.id, profile=profile, status_json=s.AsDict()))
            Status.objects.bulk_create(status_objs)
            print "loaded {} statuses".format(len(status_objs))

            print kwargs
            statuses = self.api.GetUserTimeline(profile.profile_id, **kwargs)

