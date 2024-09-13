from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class sessions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session_id = models.CharField(max_length=200)