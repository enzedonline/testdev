# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from django.contrib.auth.forms import UserCreationForm, UserChangeForm
# from .models import CustomUser

# class CustomUserAdmin(UserAdmin):
#     add_form = UserCreationForm
#     form = UserChangeForm
#     model = CustomUser
#     list_display = ['pk', 'email', 'first_name', 'last_name', 'address']
#     add_fieldsets = UserAdmin.add_fieldsets + (
#         (None, {'fields': (
#             'email', 
#             'first_name', 
#             'last_name', 
#             'address',
#             )}
#         ),
#     )
#     fieldsets = UserAdmin.fieldsets + (
#         (None, {'fields': (
#             'address', 
#             )}
#         ),
#     )

# admin.site.register(CustomUser, CustomUserAdmin)