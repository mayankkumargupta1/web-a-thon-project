from django.db import models
from django.contrib.auth.models import User


class verify_code(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.IntegerField()