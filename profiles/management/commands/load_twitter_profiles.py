import time
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
                print l.screen_name
                defaults = dict(
                    name=l.name,
                    screen_name=l.screen_name,
                    location=l.location,
                    description=l.description,
                    profile_image_url=l.profile_image_url,
                    user_json=l.AsDict()
                )
                p, created = Profile.objects.get_or_create(profile_id=l.id, defaults=defaults)
                if not created:
                    for k, v in defaults.items():
                        setattr(p, k, v)
                    p.save()

                kwargs = {'count': 200}
                try:
                    newest_status = Status.objects.filter(profile=p).order_by('id')[0]
                except IndexError:
                    pass
                else:  # don't go back beyond the newest status currently known
                    kwargs['since_id'] = newest_status.status_id
                print kwargs
                try:
                    statuses = api.GetUserTimeline(p.profile_id, **kwargs)
                except twitter.error.TwitterError as e:
                    print "twitter error {} on {}".format(e, p.screen_name)
                kwargs['max_id'] = None
                while len(statuses) > 0 and statuses[-1].id != kwargs['max_id']:
                    time.sleep(5)  # should delay enough between queries to overcome the rate limit
                    for s in statuses:
                        s_obj, created = Status.objects.get_or_create(
                            status_id=s.id, defaults={'profile': p, 'status_json': s.AsDict()}
                        )
                    kwargs['max_id'] = s_obj.status_id-1
                    print kwargs
                    statuses = api.GetUserTimeline(p.profile_id, **kwargs)
