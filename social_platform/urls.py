from django.urls import path, include
from rest_framework import routers

from social_platform.views import UserProfileViewSet, PostViewSet

router = routers.DefaultRouter()
router.register("profiles", UserProfileViewSet)
router.register("posts", PostViewSet)


urlpatterns = [
    path("", include((router.urls))),
]


app_name = "social_platform"
