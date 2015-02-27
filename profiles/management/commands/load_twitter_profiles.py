import json
from optparse import make_option

import twitter
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from profiles.models import Profile, Status

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--list',
            action='store',
            dest='list',
            help='A "username/list" of profiles to fetch'),
        make_option('--user',
            action='store',
            dest='username',
            help='A username to fetch'),
        make_option('--timeline',
            action='store_true',
            dest='timeline',
            default=False,
            help='fetch user timelines as well'),
        )

    def handle(self, *args, **options):
        api = twitter.Api(consumer_key=settings.CONSUMER_KEY,
                          consumer_secret=settings.CONSUMER_SECRET,
                          access_token_key=settings.ACCESS_TOKEN_KEY,
                          access_token_secret=settings.ACCESS_TOKEN_SECRET)
        try:
            api.VerifyCredentials()
        except twitter.error.TwitterError as e:
            self.stderr.write('Twitter authentication failed.')
            return
        if options['list']:
            if '/' not in options['list']:
                self.stderr.write(
                    'Must specify list owner screen name and list name separated by "/"'
                )
            (owner, listname) = options['list'].split('/')
            list_members = api.GetListMembers(None, listname, owner_screen_name=owner)
            for l in list_members:
                p = Profile.objects.create(name=l.name,
                                           screen_name=l.screen_name,
                                           location=l.location,
                                           description=l.description,
                                           profile_image_url=l.profile_image_url,
                                           user_json=l.AsDict())
                if l.status:
                    Status.objects.create(profile=p,
                                          status_id=l.status.id,
                                          status_json=l.status.AsDict())
