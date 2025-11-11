from django.contrib.auth.models import AbstractUser
from django.db import models
from .descriptors import EmailDescriptor, PhoneDescriptor, PriorityDescriptor

class User(AbstractUser):
    email = EmailDescriptor()
    phone = PhoneDescriptor()
    priority = PriorityDescriptor(default='LOW')

class Notification(models.Model):
    message = models.TextField()
    destinataire = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification to {self.destinataire} : {self.message[:30]}"
