from django.db import models

# Create your models here.
class Category_Book(models.Model):
    title = models.CharField(default='',max_length=255)
    slug = models.CharField(max_length=100,default='')
    description = models.TextField(default='')
    active = models.BooleanField(default=True)

class Book(models.Model):
    title = models.CharField(max_length=255,default='')
    category = models.ForeignKey(Category_Book,on_delete=models.CASCADE)
    description = models.TextField(default='')
    price = models.IntegerField(default=0)
    active = models.BooleanField(default=True)

class Variation(models.Model):
    book = models.ForeignKey(Book,on_delete=models.CASCADE)
    price = models.IntegerField(default=0)
    sale_price = models.IntegerField(default=0)
    inventory = models.IntegerField(default=0)
    active = models.BooleanField(default=True)