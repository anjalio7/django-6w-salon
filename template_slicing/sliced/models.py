from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime

# Create your models here.
class user(AbstractUser):
    pass 

class services (models.Model):
    name = models.CharField(max_length=50, unique=True)

class sub_services (models.Model):
    # service_id = models.CharField(max_length=50)
    service_id = models.ForeignKey(services, on_delete = models.CASCADE, related_name = "service_id")
    name = models.CharField(max_length=50)
    price = models.CharField(max_length=50)
    image = models.ImageField(upload_to = "images/")
    description = models.CharField(max_length=200, default='')


    class Meta:
        unique_together = ('service_id', 'name',)




class appointment (models.Model):
    # user_id = models.CharField(max_length=50)
    user_id = models.ForeignKey(user, on_delete = models.CASCADE, related_name = "user_id")
    bookingdate = models.DateTimeField(default=datetime.now())
    subservice_id = models.ForeignKey(sub_services, on_delete=models.CASCADE, related_name='subId')
    status = models.CharField(max_length=50, default='Pending')




 