import twitter

from django.conf import settings
from django.shortcuts import render

from profiles import models

# https://pbs.twimg.com/profile_images/531250423391191041/ZeS6fUev_200x200.jpeg

def home(request):
    list_members = models.Profile.objects.all()
    people = []
    for m in list_members:
        user_json = m.user_json
        user_json['small_pic'] = user_json['profile_image_url'].replace('_normal', '_bigger')
        user_json['large_pic'] = user_json['profile_image_url'].replace('_normal', '_200x200')
        people.append(user_json)
    return render(request, 'home.html', {'people': people})
