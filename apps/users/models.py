from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def __str__(self):
        return self.username

    class Meta:
        ordering = ["-is_active"]


class UserSettings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification_email = models.EmailField(blank=True, null=True)
    frequency = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username}'s settings"

    class Meta:
        verbose_name = "User settings"
        verbose_name_plural = "User settings"


class Contact(models.Model):
    subject = models.CharField(max_length=255)
    body = models.TextField()
    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    date_received = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.submitted_by.username} - {self.subject}"

    class Meta:
        verbose_name = "Contact messages"
        verbose_name_plural = "Contact messages"
