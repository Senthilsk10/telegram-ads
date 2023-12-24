from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import client

fields = list(UserAdmin.fieldsets)
fields[1] = ("personal info",{'fields':("first_name","last_name","email","client_id","client_name","client_key")})
UserAdmin.fieldsets = tuple(fields)

admin.site.register(client,UserAdmin)