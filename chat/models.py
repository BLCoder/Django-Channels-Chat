from django.contrib.auth import get_user_model
from django.db import models
from django.conf import settings 

User = get_user_model()

class Message(models.Model):
    author = models.ForeignKey(User, related_name='author_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.username

    def last_10_messages():
        return Message.objects.order_by('-timestamp').all()

class Userimage(models.Model):
	person=models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='person')
	image=models.FileField()
	
	def __str__(self):
		return self.person.username


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"Profile of {self.user.username}"