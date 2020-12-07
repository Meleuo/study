from django.contrib import admin
from crm import models
# Register your models here.
# class CustomerAdmin(admin.ModelAdmin):
#     pass

admin.site.register(models.Customer)
admin.site.register(models.ClassList)
admin.site.register(models.Campuses)