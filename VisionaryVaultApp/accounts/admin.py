from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from .forms import AdminUserCreationForm, AdminUserChangeForm
from .models import Profile

UserModel = get_user_model()


@admin.register(UserModel)
class UserAdmin(BaseUserAdmin):
    form = AdminUserChangeForm
    add_form = AdminUserCreationForm

    list_display = ('username', 'email', 'get_first_name', 'get_last_name', 'is_active', 'is_staff', 'date_joined')
    list_filter = ('is_active', 'is_staff', 'email')
    filter_horizontal = ('groups', 'user_permissions')
    search_fields = ('username', 'email', 'profile__first_name', 'profile__last_name')
    ordering = ('-date_joined',)
    readonly_fields = ('is_active', 'date_joined')

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'email', 'password1', 'password2', 'is_staff', 'is_superuser', 'groups',
                'user_permissions'),
        }),
    )

    def get_first_name(self, obj):
        return obj.profile.first_name

    def get_last_name(self, obj):
        return obj.profile.last_name

    get_first_name.short_description = 'First Name'
    get_last_name.short_description = 'Last Name'


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'full_name', 'age', 'date_of_birth', 'profile_picture', 'phone_number', 'address'
    )
    search_fields = ('user__username', 'user__email', 'first_name', 'last_name')
    readonly_fields = ('user',)

    fieldsets = (
        (None, {'fields': ('user', 'first_name', 'last_name', 'bio')}),
        ('Contact Information', {'fields': ('phone_number', 'address')}),
        ('Personal Information', {'fields': ('date_of_birth', 'profile_picture')}),
    )