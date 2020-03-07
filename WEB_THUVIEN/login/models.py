from django.db import models
from django.utils import timezone
import serial


# Create your models here.
class DocGia(models.Model):
    sex_choice=((0,"Nữ"),(1,"Nam"))
    id_DG = models.CharField(primary_key=True,max_length=8,blank=False,null=False,default="")
    ten_DG = models.CharField(max_length=100,blank=False,null=False)
    gioitinh = models.IntegerField(choices=sex_choice,default=0)
    email_DG = models.EmailField(max_length=200,blank=False,null=False)
    CMND=models.CharField(max_length=20,blank=False,null=False)
    phone=models.CharField(max_length=15,blank=False,null=False)
    time_create=models.DateTimeField(default=timezone.datetime.now())

    def __str__(self):
        return self.id_DG


# Models Loại Sách
class Category_Book(models.Model):
    title = models.CharField(default='',max_length=255)
    slug = models.CharField(max_length=100,default='')
    description = models.TextField(default='')
    active = models.BooleanField(default=True)

# Model Sách
class Book(models.Model):
    id_book=models.CharField(max_length=10,default='')
    title = models.CharField(max_length=255,default='')
    category = models.ForeignKey(Category_Book,on_delete=models.CASCADE)
    description = models.TextField(default='')
    price = models.IntegerField(default=0)
    image_book=models.ImageField(default=True)
    active = models.BooleanField(default=True)

# Model sự thay đổi những thứ liên quan tới sách
class Variation(models.Model):
    book = models.ForeignKey(Book,on_delete=models.CASCADE)
    price = models.IntegerField(default=0)
    sale_price = models.IntegerField(default=0)
    inventory = models.IntegerField(default=0)
    active = models.BooleanField(default=True)