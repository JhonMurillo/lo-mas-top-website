from django.db import models
# from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):

    YOUTUBE='YOUTUBE'
    FACEBOOK='FACEBOOK'
    INSTAGRAM='INSTAGRAM'
    OTROS='OTROS'
    SOURCES = (
      (YOUTUBE, 'Youtube'),
      (FACEBOOK, 'Facebook'),
      (INSTAGRAM, 'Instagram'),
      (OTROS, 'Otros')
      )

    # user = models.ForeignKey(User,on_delete=models.CASCADE)
    # profile = models.ForeignKey('users.Profile',on_delete=models.CASCADE)

    title = models.CharField(max_length=255)
    # photo = models.ImageField(upload_to='post/photos')
    description = models.CharField(max_length=4000, null=True)
    source  = models.CharField(max_length=20, choices=SOURCES, default=YOUTUBE)

    link = models.CharField(max_length=255, null=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

def __str__(self):
    return self.link


# class Publish