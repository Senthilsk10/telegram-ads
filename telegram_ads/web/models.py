from django.db import models
from client.models import File,verified_groups,client
import secrets

from django.urls import reverse

class Link_to_file(models.Model):
    file = models.ForeignKey(File, related_name='File_info', on_delete=models.CASCADE,null=False)
    user_chat_id = models.IntegerField(blank=True, null=False)
    group_id = models.ForeignKey(verified_groups, related_name='group_details', on_delete=models.CASCADE)
    param = models.CharField(max_length=12,default=secrets.token_urlsafe(12), editable=False, unique=True)
    is_shared = models.BooleanField(default=False,blank=True, null=False)

    def save(self, *args, **kwargs):
        # Generate and set the unique key only if it doesn't exist or if it's already in use
        if not self.param or Link_to_file.objects.filter(param=self.param).exists():
            self.param = secrets.token_urlsafe(12)  # You may adjust the length as needed

        if self.is_shared:
            super(Link_to_file, self).delete()
        else:
            super(Link_to_file, self).save(*args, **kwargs)
    
    def get_link(self):
        url = reverse('web:share_file', kwargs = {'param':self.param})
        return f'https://stunning-space-tribble-5w5xx46q4qwfwx9-8000.preview.app.github.dev/{url}'
class Analytics(models.Model):
    total_file_sent = models.IntegerField(blank=True, null=False,default=0)
    client = models.ForeignKey(client, related_name='analytics_referenced_client', on_delete=models.CASCADE)
