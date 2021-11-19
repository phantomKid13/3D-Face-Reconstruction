from django.db import models

# Create your models here.
class Feedback(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length = 100)
    message = models.CharField(max_length=1000)