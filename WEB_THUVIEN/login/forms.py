from django import forms
from django.core.exceptions import ObjectDoesNotExist


from .models import DocGia,Book
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
        raise forms.TextInput.ValidationError("ID đã tồn taị")


class Sach(forms.ModelForm):
    class Meta:
        model=Book
        fields =('id_book','title','category','description','image_book','active',)

        def clean_idSach(self):
            id_book = self.cleaned_data['id_book']
            try:
                Book.objects.get(id_book=id_book)
            except ObjectDoesNotExist:
                return id_book
            raise forms.ValidationError("ID đã tồn taị")