from django.contrib import admin
from app01 import models
# Register your models here.

admin.site.register(models.Books)
admin.site.register(models.Press)
admin.site.register(models.Author)
