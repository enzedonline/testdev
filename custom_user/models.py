# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import AbstractUser
from django.db import models
# from wagtail.contrib.modeladmin.options import (
#     ModelAdmin, modeladmin_register, ModelAdminGroup
# )
# from wagtail.admin.panels import FieldPanel
# from wagtail.core.fields import RichTextField

class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.street}, {self.city}, {self.state} {self.postal_code}"

class CustomUser(AbstractUser):
    address = models.OneToOneField(Address, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

# class CustomUserModelAdmin(UserAdmin):
#     model = CustomUser

# class CustomUserGroup(ModelAdminGroup):
#     menu_label = 'Users'
#     menu_icon = 'user'
#     items = [CustomUserModelAdmin]

# modeladmin_register(CustomUserGroup)
