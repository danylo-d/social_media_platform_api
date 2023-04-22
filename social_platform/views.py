from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from social_platform.models import UserProfile
from social_platform.permissions import IsOwnerOrReadOnly
from social_platform.serializers import (
    UserProfileSerializer,
    UserProfileListSerializer,
    FollowersSerializer,
    SubscriptionSerializer,
)


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)

    def get_queryset(self):
        username = self.request.query_params.get("username")

        queryset = self.queryset

        if username:
            queryset = queryset.filter(username__icontains=username)
        return queryset.distinct()

    def get_serializer_class(self):
        if self.action == "list":
            return UserProfileListSerializer

        if self.action == "show_followers":
            return FollowersSerializer

        if self.action == "show_subscriptions":
            return SubscriptionSerializer

        return UserProfileSerializer

    @action(methods=["GET"], detail=True, url_path="followers")
    def show_followers(self, request, pk=None):
        profile = self.get_object()
        serializer = self.get_serializer_class()(profile.followers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=["GET"], detail=True, url_path="subscriptions")
    def show_subscriptions(self, request, pk=None):
        profile = self.get_object()
        serializer = self.get_serializer_class()(profile.subscription, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=["GET"], detail=True, url_path="follow_or_unfollow")
    def follow_or_unfollow(self, request, pk=None):
        profile = self.get_object()
        user = request.user
        if user.is_authenticated:
            if profile.user != request.user:
                if user not in profile.followers.all():
                    profile.followers.add(user)
                    user.user_profile.subscription.add(profile.user)

                    return Response(
                        {"message": f"You Followed {profile.username}"},
                        status=status.HTTP_200_OK,
                    )
                else:
                    profile.followers.remove(user)
                    user.user_profile.subscription.remove(profile.user)

                    return Response(
                        {"message": f"You stopped following {profile.username}"},
                        status=status.HTTP_200_OK,
                    )
            return Response(
                {"message": f"You can't follow yourself"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(status=status.HTTP_401_UNAUTHORIZED)
