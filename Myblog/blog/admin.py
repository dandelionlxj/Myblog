from django.contrib import admin
from . import models
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display=['title','create_time','modified_time','category','author']

admin.site.register(models.Post,PostAdmin)
admin.site.register(models.Category)
admin.site.register(models.Tag)