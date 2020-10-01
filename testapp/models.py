from django.db import models


# Create your models here.
class StudentModel(models.Model):
    sno = models.IntegerField()
    sname = models.CharField(max_length=50)
    smarks = models.IntegerField()
    saddress = models.CharField(max_length=100)
