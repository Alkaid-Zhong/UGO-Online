from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import User, Address

admin.site.register(User)
admin.site.register(Address)
