from django.contrib import admin
from Sprint2 import models

# Register your models here.
admin.site.register(models.User)
admin.site.register(models.Course)
admin.site.register(models.Section)
admin.site.register(models.Ta)
admin.site.register(models.Enroll)
admin.site.register(models.CourseAssignment)