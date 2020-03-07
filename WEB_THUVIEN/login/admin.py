from django.contrib import admin
from .models import DocGia,Book,Category_Book,Variation
# Register your models here.
admin.site.register(DocGia)
admin.site.register(Book)
admin.site.register(Category_Book)
admin.site.register(Variation)