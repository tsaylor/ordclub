import twitter

from django.conf import settings
from django.shortcuts import render

from profiles import models

# https://pbs.twimg.com/profile_images/531250423391191041/ZeS6fUev_200x200.jpeg

def home(request):
    list_members = models.Profile.objects.all()
    people = (dict(name=m.name,
                   pic=m.user_json['profile_image_url'].replace('_normal', '_bigger'),
                   screen_name=m.screen_name)
              for m in list_members)
    return render(request, 'home.html', {'people': people})
