from django.contrib import admin
from .models import Subreddit, SubscriberHistory


admin.site.register(Subreddit)
admin.site.register(SubscriberHistory)
