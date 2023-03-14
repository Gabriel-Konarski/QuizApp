from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Category)
admin.site.register(models.Quiz)
admin.site.register(models.Question)
admin.site.register(models.Answer)
admin.site.register(models.Profile)
admin.site.register(models.DoneQuizes)
admin.site.register(models.Type)
