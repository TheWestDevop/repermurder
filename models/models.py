from django.db import models
from django.utils.timezone import now
# Create your models here.
class LoginDetails(models.Model):
      email   = models.EmailField(max_length=200)
      password   = models.CharField(max_length=300)
      secret     = models.CharField(max_length=200)
      ip         = models.CharField(max_length=200)
      created_at = models.DateTimeField(default=now)
    

