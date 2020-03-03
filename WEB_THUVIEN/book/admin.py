from django.contrib import admin
from .models import Category_Book,Variation,Book
# Register your models here.
admin.site.register(Book)
admin.site.register(Category_Book)
admin.site.register(Variation)