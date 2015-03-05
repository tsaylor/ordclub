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
        self.api = twitter.Api(consumer_key=settings.CONSUMER_KEY,
                          consumer_secret=settings.CONSUMER_SECRET,
                          access_token_key=settings.ACCESS_TOKEN_KEY,
                          access_token_secret=settings.ACCESS_TOKEN_SECRET)
        try:
            self.api.VerifyCredentials()
        except twitter.error.TwitterError as e:
            self.stderr.write('Twitter authentication failed.')
            return
        if options['list']:
            if '/' not in options['list']:
                self.stderr.write(
                    'Must specify list owner screen name and list name separated by "/"'
                )
            (owner, listname) = options['list'].split('/')
            list_members = self.api.GetListMembers(None, listname, owner_screen_name=owner)
            for l in list_members:
                print l.screen_name
                profile = self.save_user(l)
                self.get_user_timeline(profile)
        elif options['username']:
            twitter_user = self.api.GetUser(screen_name=options['username'])
            profile = self.save_user(twitter_user)
            print profile.screen_name
            self.get_user_timeline(profile)

    def save_user(self, user):
        """ takes a twitter api user object, returns a Profile model object """
        defaults = dict(
            name=user.name,
            screen_name=user.screen_name,
            location=user.location,
            description=user.description,
            profile_image_url=user.profile_image_url,
            user_json=user.AsDict()
        )
        p, created = Profile.objects.get_or_create(profile_id=user.id, defaults=defaults)
        if not created:
            for k, v in defaults.items():
                setattr(p, k, v)
            p.save()
        return p

    def get_user_timeline(self, profile):
        """ takes a Profile model object, captures all the profile's statuses. """
        kwargs = {'count': 200}
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
        kwargs['max_id'] = None
        while len(statuses) > 0 and statuses[-1].id != kwargs['max_id']:
            time.sleep(5)  # should delay enough between queries to overcome the rate limit
            for s in statuses:
                s_obj, created = Status.objects.get_or_create(
                    status_id=s.id, defaults={'profile': profile, 'status_json': s.AsDict()}
                )
            kwargs['max_id'] = s_obj.status_id-1
            print kwargs
            statuses = self.api.GetUserTimeline(profile.profile_id, **kwargs)

