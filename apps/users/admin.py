from django.contrib import admin
from .models import User, UserSettings, Contact


admin.site.register(User)
admin.site.register(UserSettings)
admin.site.register(Contact)