from django.db import models
from django.utils import timezone
import serial


# Create your models here.
class DocGia(models.Model):
    sex_choice=((0,"Nữ"),(1,"Nam"))
    id_DG = models.CharField(primary_key=True,max_length=20,blank=False,null=False,default="")
    ten_DG = models.CharField(max_length=100,blank=False,null=False)
    gioitinh = models.IntegerField(choices=sex_choice,default=0)
    email_DG = models.EmailField(max_length=200,blank=False,null=False)
    CMND=models.CharField(max_length=20,blank=False,null=False)
    phone=models.CharField(max_length=15,blank=False,null=False)
    time_create=models.DateTimeField(default=timezone.datetime.now())

    def __str__(self):
        return self.id_DG