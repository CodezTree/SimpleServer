from django.db import models

# Create your models here.


class User(models.Model):
    user_token = models.CharField(max_length=200, default="")
    firebase_token = models.CharField(max_length=200, default="")
    user_sum_temp = models.TextField(default="")  # Temp JSON Array
    temp_num = models.CharField(max_length=4, default="")