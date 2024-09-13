from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class feedback(models.Model):
    name = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    description = models.TextField(max_length=4000)
    def __str__(self) -> str:
        return f'Name: {self.name}, Position: {self.position}'
    
class contact_us(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(max_length=4000)

    def __str__(self) -> str:
        return f'user: {self.user.username}, message: {self.message}'