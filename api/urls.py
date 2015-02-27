from django.conf.urls import url, include
from django.contrib.auth.models import User
from profiles.models import Profile
from rest_framework import routers, serializers, viewsets

# Serializers define the API representation.
class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    pic_url = serializers.DictField(source='get_pic', child=serializers.CharField())

    class Meta:
        model = Profile
        fields = tuple(
            a.name for a in Profile._meta.fields if not a.name.startswith('_')) + ('pic_url',)


# ViewSets define the view behavior.
class ProfileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'profiles', ProfileViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]