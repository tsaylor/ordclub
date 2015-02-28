import twitter

from django.conf import settings
from django.shortcuts import render

from profiles import models

# https://pbs.twimg.com/profile_images/531250423391191041/ZeS6fUev_200x200.jpeg
# http://spiffygif.com/?color=000&lines=10&length=15&radius=20&width=4

def home(request):
    list_members = models.Profile.objects.all()
    return render(request, 'home.html', {'people': list_members})
