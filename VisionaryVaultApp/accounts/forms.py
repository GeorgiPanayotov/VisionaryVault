from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from VisionaryVaultApp.accounts.models import Profile
from VisionaryVaultApp.accounts.validators import NameValidator  # Ensure this validator is defined

User = get_user_model()


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        validators=[NameValidator()],
        required=True,
    )
    last_name = forms.CharField(
        validators=[NameValidator()],
        required=True,
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        labels = {
            'username': 'Username',
            'email': 'Email',
            'password': 'Password',
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken.")
        if len(username) > 15:
            raise ValidationError("Username cannot be longer than 15 characters.")
        if '@' in username:
            raise ValidationError("Username cannot contain '@'.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already being used.")
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customizing password fields with placeholders instead of help_text and default validation messages
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None

        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Try complex password with at least 8 symbols, do not use only digits',
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Enter the same password as above, for verification.',
        })

        # Optionally, remove default error messages and replace them with your own
        self.fields['password1'].error_messages = {'required': 'Try complex password with at least 8 symbols, do not use only digits'}
        self.fields['password2'].error_messages = {'required': 'Enter the same password as above, for verification.'}


# User update form for profile-related fields
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']  # Only allow username to be updated

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['readonly'] = True
        self.fields['username'].help_text = None


# Profile update form for profile-specific fields
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['first_name', 'last_name', 'user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


# Custom password change form
class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label=_("Old password"), widget=forms.PasswordInput)
    new_password1 = forms.CharField(label=_("New password"), widget=forms.PasswordInput)
    new_password2 = forms.CharField(label=_("Confirm new password"), widget=forms.PasswordInput)

    class Meta:
        model = User  # Reference the custom user model
        fields = ('old_password', 'new_password1', 'new_password2')


class CustomLoginForm(forms.Form):
    username_or_email = forms.CharField(label='Username or Email', max_length=254)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def __init__(self, *args, request=None, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        self.request = request  # Store the request object if needed

    def clean_username_or_email(self):
        username_or_email = self.cleaned_data.get('username_or_email')
        if not User.objects.filter(username=username_or_email).exists() and not User.objects.filter(
                email=username_or_email).exists():
            raise forms.ValidationError("TIP: Check for typos in your username or email.")
        return username_or_email

    def clean_password(self):
        username_or_email = self.cleaned_data.get('username_or_email')
        password = self.cleaned_data.get('password')

        # Skip validation if username_or_email is not yet valid
        if not username_or_email:
            return password

        # Attempt to authenticate user
        user = authenticate(username=username_or_email, password=password)
        if user is None:
            # If no user was found, check if the username_or_email is an email
            try:
                user_by_email = User.objects.get(email=username_or_email)
                user = authenticate(username=user_by_email.username, password=password)
            except User.DoesNotExist:
                user = None

        if user is None:
            raise forms.ValidationError("Check Caps Lock. Passwords are case-sensitive.")
        return password


class EmailChangeForm(forms.ModelForm):
    email = forms.EmailField(required=True, label="New Email")

    class Meta:
        model = User  # Ensure it's set to your custom user model
        fields = ['email']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
