import twitter

from django.conf import settings
from django.shortcuts import render

from profiles import models

# https://pbs.twimg.com/profile_images/531250423391191041/ZeS6fUev_200x200.jpeg

def home(request):
    list_members = models.Profile.objects.all()
    return render(request, 'home.html', {'people': list_members})
