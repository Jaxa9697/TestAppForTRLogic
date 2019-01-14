from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateField(null=True, blank=True)
    about = models.CharField(max_length=1000, null=True)
    avatar = models.ImageField(upload_to='%Y/%m/%d/', default='default-avatar.png')
