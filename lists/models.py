from django.db import models

# Create your models here.
class Item(models.Model):
    '''list elemnt'''
    text = models.TextField(default='')
