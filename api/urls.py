from django.conf.urls import url, include
from django.contrib.auth.models import User
from django.db.models import Q

from rest_framework import routers, serializers, viewsets

from profiles.models import Profile


# Serializers define the API representation.
class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    pic_url = serializers.DictField(source='get_pic', child=serializers.CharField())

    class Meta:
        model = Profile
        fields = tuple(
            a.name for a in Profile._meta.fields if not a.name.startswith('_')) + ('pic_url',)


# ViewSets define the view behavior.
class ProfileViewSet(viewsets.ReadOnlyModelViewSet):
    model = Profile
    serializer_class = ProfileSerializer

    def get_queryset(self):
        search = self.request.GET.get('search', '')
        qs = self.model.objects.all()
        if search != '':
            qs = qs.filter(Q(name__icontains=search) |
                           Q(description__icontains=search))
        return qs


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'profiles', ProfileViewSet, base_name='profile')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]