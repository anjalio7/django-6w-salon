from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

# Create your models here.
class User(AbstractUser):
    pass

    def clean(self):
        if (not len(self.username) > 3):
            raise ValidationError(('title not '))
            # raise ValidationError()
    
    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)