from django.db import models

# Create your models here.
class List(models.Model):
#    list_id = models.ForeignKey('Item', on_delete=models.CASCADE)
    pass

class Item(models.Model):
    '''list elemnt'''
    text = models.TextField(default='')
    list = models.ForeignKey(List, default=None, on_delete=models.CASCADE)
