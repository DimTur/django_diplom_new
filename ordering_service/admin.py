from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Address, Contact, Shop, Category, Product, ProductInfo, Parameter, ProductInfoParameter, \
    Order, OrderProduct


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


class ContactInline(admin.TabularInline):
    model = Contact


admin.site.register(Address)
admin.site.register(Contact)
admin.site.register(Shop)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductInfo)
admin.site.register(Parameter)
admin.site.register(ProductInfoParameter)
admin.site.register(Order)
admin.site.register(OrderProduct)
admin.site.register(CustomUser, CustomUserAdmin)
