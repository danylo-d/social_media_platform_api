from rest_framework import serializers


from social_platform.models import UserProfile, Post
from user.models import User


class FollowersSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user_profile.username", read_only=True)
    full_name = serializers.CharField(source="user_profile.full_name", read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "full_name",
        )


class SubscriptionSerializer(FollowersSerializer):
    pass


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = (
            "username",
            "first_name",
            "last_name",
            "date_of_birth",
            "bio",
            "profile_picture",
            "amount_of_followers",
            "amount_of_subscriptions",
        )
        read_only_fields = ("user", "followers", "subscription")

    def validate(self, attrs):
        data = super(UserProfileSerializer, self).validate(attrs=attrs)
        user_profile_exists = UserProfile.objects.filter(
            user=self.context["request"].user
        ).exists()
        if user_profile_exists and self.context["request"].method == "POST":
            raise serializers.ValidationError("You already have a profile")

        return data


class UserProfileListSerializer(UserProfileSerializer):
    class Meta:
        model = UserProfile
        fields = (
            "id",
            "full_name",
            "username",
            "amount_of_followers",
            "amount_of_subscriptions",
        )


class PostSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.user_profile.username", read_only=True)
    full_name = serializers.CharField(source="user.user_profile.full_name", read_only=True)

    class Meta:
        model = Post
        fields = ("id", "user", "full_name", "content", "image", "hashtags", "created_at")
        read_only_fields = ("user",)


class PostListSerializer(PostSerializer):
    user = serializers.CharField(source="user.user_profile.username", read_only=True)

    class Meta:
        model = Post
        fields = (
            "id",
            "user",
            "image",
            "content_preview",
            "hashtags",
            "created_at",
        )
        read_only_fields = ("user",)
