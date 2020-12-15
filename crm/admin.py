from django.contrib import admin
from crm import models
# Register your models here.
# class CustomerAdmin(admin.ModelAdmin):
#     pass

admin.site.register(models.Customer)
admin.site.register(models.ClassList)
admin.site.register(models.Campuses)
admin.site.register(models.ConsultRecord)
admin.site.register(models.Enrollment)
admin.site.register(models.CourseRecord)
