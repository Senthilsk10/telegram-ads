from django.db import models
from django.contrib.auth.models import AbstractUser,User

class client(AbstractUser):
    client_id  = models.BigIntegerField(blank=True, null=True,unique=True)
    client_name  = models.CharField(max_length=45, blank=True, null=True)
    client_key = models.CharField(max_length = 30,blank=True, null=True)
