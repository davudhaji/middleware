from django.contrib import admin
from acceptance import models

# Register your models here

admin.site.register(models.Sign)
admin.site.register(models.QmaticLog)
admin.site.register(models.ServiceRate)
admin.site.register(models.PersonalInfo)