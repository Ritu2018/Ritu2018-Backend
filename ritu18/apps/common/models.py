from django.db import models


# Create your models here.

class Profile(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=14, unique=True)
    email = models.EmailField()
    college = models.CharField(max_length=900, null=True)

    def __str__(self):
        return self.name + " : " + self.phone
