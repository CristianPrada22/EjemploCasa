from django.contrib import admin
from .models import Person, Role, PersonRole

# Register your models here.

admin.site.register(Person)
admin.site.register(Role)
admin.site.register(PersonRole)