from django.conf import settings
from django.db import models


class UserProfile(models.Model):
    username = models.CharField(max_length=63, unique=True)
    first_name = models.CharField(max_length=63)
    last_name = models.CharField(max_length=63)
    date_of_birth = models.DateField()
    bio = models.TextField(null=True, blank=True)
    profile_picture = models.ImageField(blank=True, null=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_profile"
    )
    followers = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="user_followers", blank=True, null=True
    )
    subscription = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="user_subscription",
        blank=True,
        null=True,
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
