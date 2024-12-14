from django.contrib import admin

# Register your models here.
from .models import Role, Bidding, UserProfile

admin.site.register(UserProfile)
admin.site.register(Role)
admin.site.register(Bidding)