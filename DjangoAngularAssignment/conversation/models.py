from django.db import models
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.models import User


class Conversations(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    created_by = models.ForeignKey(User, related_name='created_by')
    created_for = models.ForeignKey(User, related_name='created_for')

    def __str__(self):
        return str(self.created_by)+' - '+str(self.created_for)


class Conversation(models.Model):
    message = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    modified_at = models.DateTimeField(blank=True, default=timezone.now)
    user = models.ForeignKey(User)
    conversation = models.ForeignKey(Conversations)
    archive = models.BooleanField(default=False)

    def __str__(self):
        return self.message+' - '+str(self.created_at)



