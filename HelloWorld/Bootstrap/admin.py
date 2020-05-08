from django.contrib import admin

# Register your models here.

from Bootstrap.models import Employee


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'eid', 'ename', 'econtact')


admin.site.register(Employee, EmployeeAdmin)  # Employee is registered
