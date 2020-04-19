from django.contrib import admin

# Register your models here.
from .models import Message,Userimage,Profile

admin.site.register(Message)
admin.site.register(Userimage)
admin.site.register(Profile)