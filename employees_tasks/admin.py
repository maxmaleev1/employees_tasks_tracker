from django.contrib import admin
from .models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'position', 'user']
    fields = ['full_name', 'position', 'user']  # Поля, которые будут отображаться в форме
