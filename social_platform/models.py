import os
import uuid

from django.conf import settings
from django.db import models
from django.utils.text import slugify


def profile_picture_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)

    filename = f"{slugify(instance.username)}-{uuid.uuid4()}.{extension}"

    return os.path.join("uploads/profile_picture/", filename)


def post_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)

    filename = f"{slugify(instance.id)}-{uuid.uuid4()}.{extension}"

    return os.path.join("uploads/post_image/", filename)


class UserProfile(models.Model):
    username = models.CharField(max_length=63, unique=True)
    first_name = models.CharField(max_length=63)
    last_name = models.CharField(max_length=63)
    date_of_birth = models.DateField()
    bio = models.TextField(null=True, blank=True)
    profile_picture = models.ImageField(
        blank=True, null=True, upload_to=profile_picture_image_file_path
    )
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_profile"
    )
    followers = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="user_followers", blank=True
    )
    subscription = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="user_subscription",
        blank=True,
    )

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def amount_of_followers(self):
        return self.followers.count()

    @property
    def amount_of_subscriptions(self):
        return self.subscription.count()

    def save(self, *args, **kwargs):
        self.pk = self.user.pk
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"


class Post(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts"
    )
    content = models.TextField()
    image = models.ImageField(blank=True, null=True, upload_to=post_image_file_path)
    created_at = models.DateTimeField(auto_now_add=True)
    hashtags = models.CharField(blank=True, max_length=63)

    class Meta:
        ordering = ["-created_at"]

    @property
    def content_preview(self):
        return self.content[:51]

    def __str__(self):
        return f"Post by {self.user.user_profile.username} on {self.created_at}"
