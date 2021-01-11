from django.db import models


class Subreddit(models.Model):
    name = models.CharField(max_length=75)
    description = models.TextField(blank=True, null=True)
    banner_img = models.CharField(max_length=200, blank=True, null=True)
    flairs = models.CharField(max_length=200, blank=True, null=True)
    url = models.CharField(max_length=75)
    creation_date = models.DateTimeField(blank=True)
    last_modified = models.DateTimeField(auto_now=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.url}"

    class Meta:
        ordering = ["-date_added"]


class SubscriberHistory(models.Model):
    subreddit = models.ForeignKey(Subreddit, on_delete=models.CASCADE)
    subscriber_count = models.IntegerField()
    date_recorded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subreddit} - {self.subscriber_count}"

    class Meta:
        verbose_name = "Subscriber History"
        verbose_name_plural = "Subscriber History"
