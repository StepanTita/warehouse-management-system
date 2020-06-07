# Register your models here.
from django.contrib import admin
from django.contrib.auth.models import Group

# admin.site.register(DateNotifications)
from users.models import Employee, Position

admin.site.site_header = 'Coordinate A.'
admin.site.unregister(Group)
admin.site.register(Employee)
admin.site.register(Position)
