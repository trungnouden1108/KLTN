from rest_framework import serializers

from .models import DocGia,Cart,Book,Category_Book

class DocGia_Serializer(serializers.ModelSerializer):
    class Meta:
        model=DocGia
        fields=('id_DG','ten_DG','gioitinh','email_DG','CMND','phone','image_user','money_user')