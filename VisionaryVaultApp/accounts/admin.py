from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from .forms import UserChangeForm, UserCreationForm


UserModel = get_user_model()


@admin.register(UserModel)
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('username', 'email', 'get_first_name', 'get_last_name', 'is_active', 'is_staff')
    list_filter = ('is_active', 'is_staff', 'email')
    filter_horizontal = ('groups', 'user_permissions')
    search_fields = ('username', 'email', 'profile__first_name', 'profile__last_name')
    ordering = ('-profile__date_of_birth',)
    readonly_fields = ('username', 'email', 'is_active', 'is_staff')

    def get_first_name(self, obj):
        return obj.profile.first_name

    def get_last_name(self, obj):
        return obj.profile.last_name

    get_first_name.short_description = 'First Name'
    get_last_name.short_description = 'Last Name'
