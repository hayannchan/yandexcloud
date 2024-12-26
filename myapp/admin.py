from django.contrib import admin

from .models import File


class FileAdmin(admin.ModelAdmin):
    list_display = ('link', 'upload_date', 'hash')

admin.site.register(File, FileAdmin)
