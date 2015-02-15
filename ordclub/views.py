import twitter

from django.conf import settings
from django.shortcuts import render

def home(request):
    api = twitter.Api(consumer_key=settings.CONSUMER_KEY,
                      consumer_secret=settings.CONSUMER_SECRET,
                      access_token_key=settings.ACCESS_TOKEN_KEY,
                      access_token_secret=settings.ACCESS_TOKEN_SECRET)
    list_members = api.GetListMembers(
        None, 'ord-campers', owner_screen_name='therealfitz')
    people = (dict(name=m.name,
                   pic=m.profile_image_url.replace('_normal', '_bigger'),
                   screen_name=m.screen_name)
              for m in list_members)
    return render(request, 'home.html', {'people': people})
