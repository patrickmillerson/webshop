from django.contrib import admin
from .models import Product, CustomUser, UserProfile

# Register your models here.
admin.site.register(Product)
admin.site.register(CustomUser)
admin.site.register(UserProfile)