from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'first_name', 'last_name', 'is_active', 'is_staff')
    search_fields = ('phone_number', 'first_name', 'last_name')
    list_filter = ('is_active', 'is_staff')



