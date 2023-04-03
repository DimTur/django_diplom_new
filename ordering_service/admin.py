from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Address, Contact


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('last_name', 'first_name', 'patronymic', 'company', 'position', 'type')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'password1', 'password2', 'is_staff', 'is_active', 'last_name', 'first_name', 'patronymic',
                'company', 'position', 'type', 'groups', 'user_permissions'
            )
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)


class AddressInline(admin.TabularInline):
    model = Address


class ContactAdmin(admin.ModelAdmin):
    inlines = [AddressInline]


admin.site.register(Contact, ContactAdmin)
admin.site.register(Address)

admin.site.register(CustomUser, CustomUserAdmin, Address)
