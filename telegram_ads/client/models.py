from django.db import models
from django.contrib.auth.models import AbstractUser,User
import secrets

class client(AbstractUser):
    client_id  = models.BigIntegerField(blank=True, null=True,unique=True)
    client_name  = models.CharField(max_length=45, blank=True, null=True)
    client_key = models.CharField(max_length=24,default=secrets.token_urlsafe(24), editable=False, unique=True)

    def save(self, *args, **kwargs):
        # Generate and set the unique key only if it doesn't exist
        if not self.client_key:
            self.your_field = secrets.token_urlsafe(24)
        super().save(*args, **kwargs)


class File(models.Model):
    file_name = models.CharField(max_length=45,blank=True, null=True)
    series_movie = models.CharField(max_length=45,blank=True, null=True)
    part =  models.IntegerField(blank=True,null=True)
    season =  models.IntegerField(blank=True,null=True)
    episode =  models.IntegerField(blank=True,null=True)
    language = models.CharField(max_length=45,blank=True, null=True)
    quality = models.CharField(max_length=45,blank=True, null=True)
    file_id = models.CharField(max_length=200,blank=True, null=True)
    file_size = models.DecimalField(max_digits=10,decimal_places=4,blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    client = models.ForeignKey(client,on_delete=models.CASCADE)