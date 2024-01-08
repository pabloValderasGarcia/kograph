from django.contrib import admin
from .models import User, File

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass

@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    pass