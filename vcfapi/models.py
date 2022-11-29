from django.db import models

# Create your models here.
class MyUser(models.Model):
    def save(self):
        pass
    objects = None
    username = "test"
    is_authenticated = False
