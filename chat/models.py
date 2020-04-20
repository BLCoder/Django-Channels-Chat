from django.contrib.auth import get_user_model
from django.db import models
from django.conf import settings 
from django.db.models.signals import post_save
from django.dispatch import receiver


User = get_user_model()

class Message(models.Model):
    author = models.ForeignKey(User, related_name='author_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.username

    def last_10_messages():
        return Message.objects.order_by('-timestamp').all()[:10]

class Userimage(models.Model):
	person=models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='person')
	image=models.FileField(default='default.jpg')
	
	def __str__(self):
		return self.person.username


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    status = models.BooleanField(default=False)
    status_up = models.BooleanField(default=True)

    def __str__(self):
        return f"Profile of {self.user.username}"


# get singal id new user registered
@receiver(post_save, sender=User)
def new_user(sender, instance, created, **kwargs):
    if kwargs.get('created',True):
        Profile.objects.get_or_create(user=instance)
        Userimage.objects.get_or_create(person=instance)
        print("Profile is created...")
