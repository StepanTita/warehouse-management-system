from django.contrib import admin

from .models import Cargo, Cell, Storage, Company, Category, Categorization

admin.site.register(Cargo)
admin.site.register(Cell)
admin.site.register(Storage)
admin.site.register(Company)
admin.site.register(Category)
admin.site.register(Categorization)
