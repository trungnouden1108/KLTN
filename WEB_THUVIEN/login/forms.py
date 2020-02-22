from django import forms
from django.core.exceptions import ObjectDoesNotExist


from .models import DocGia
import serial

class Register(forms.ModelForm):
    class Meta:
        model = DocGia
        fields=('id_DG','ten_DG','gioitinh','email_DG','CMND','phone',)

    def clean_idDG(self):
        id_DG=self.cleaned_data['id_DG']
        try:
            DocGia.objects.get(id_DG=id_DG)
        except ObjectDoesNotExist:
            return id_DG
        raise forms.ValidationError("ID đã tồn taị")


