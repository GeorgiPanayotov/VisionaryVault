from django.contrib.auth import logout, authenticate, login, get_user_model, views as auth_views
from django.contrib.auth.views import LoginView, PasswordChangeDoneView, PasswordChangeView, PasswordResetView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import UpdateView, TemplateView
from .forms import UserRegistrationForm, UserUpdateForm, CustomLoginForm, EmailChangeForm, ProfileUpdateForm, \
    CustomPasswordResetForm
from .models import Profile

User = get_user_model()


class AuthService:
    @staticmethod
    def authenticate_user(request, username_or_email, password):
        user = authenticate(username=username_or_email, password=password)

        if user is None:
            # Attempt to find user by email
            try:
                user_by_email = User.objects.get(email=username_or_email)
                user = authenticate(request, username=user_by_email.username, password=password)
            except User.DoesNotExist:
                pass

        return user


class ProfileService:
    @staticmethod
    def delete_user(user):
        # Implement any necessary cleanup before user deletion
        user.delete()


class CustomLogoutView(View):
    def post(self, request):
        logout(request)
        messages.success(request, "You have been logged out successfully.")
        return redirect('home')


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    form_class = CustomLoginForm

    def form_valid(self, form):
        username_or_email = form.cleaned_data['username_or_email']
        password = form.cleaned_data['password']

        user = AuthService.authenticate_user(self.request, username_or_email, password)

        if user is None:
            try:
                user_by_email = User.objects.get(email=username_or_email)
                user = authenticate(self.request, username=user_by_email.username, password=password)
            except User.DoesNotExist:
                pass

        if user is not None:

            if user.groups.filter(name='Banned users').exists() and not user.is_active:
                messages.error(self.request, "Your account has been banned or is inactive. Please contact support.")
                return self.form_invalid(form)

            login(self.request, user)
            messages.success(self.request, "Login is successful!")
            return redirect('home')

        messages.error(self.request, "Invalid username/email or password.")
        return self.form_invalid(form)


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def edit_profile(request):
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile_details')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'accounts/edit_profile.html', context)


@login_required
def profile_details(request):
    # Assuming Profile has a one-to-one relationship with the User model
    profile = get_object_or_404(Profile, user=request.user)
    return render(request, 'accounts/profile_details.html', {'profile': profile})


@login_required
def delete_profile(request):
    if request.method == 'POST':
        user = request.user
        ProfileService.delete_user(user)
        messages.success(request, "Your profile has been deleted successfully.")
        logout(request)
        return redirect('home')

    return render(request, 'accounts/delete_profile.html')


class CustomPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'accounts/change_password_done.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add custom context or messages to the success page if needed
        context['message'] = "Your password was updated successfully!"
        return context


class CustomChangePasswordView(PasswordChangeView):
    template_name = 'accounts/change_password.html'
    success_url = reverse_lazy('password_change_done')

    def form_valid(self, form):
        # You can add extra behavior here, e.g., logging or notifications
        return super().form_valid(form)


class EmailChangeView(UpdateView):
    model = User  # Ensure this references your custom user model
    form_class = EmailChangeForm
    template_name = 'accounts/change_email.html'  # Ensure this path is correct
    success_url = reverse_lazy('email_change_done')  # Redirect after successful email change

    def get_object(self, queryset=None):
        return self.request.user


class EmailChangeDoneView(TemplateView):
    template_name = 'accounts/change_email_done.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = "Your email address was updated successfully!"
        return context


class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'accounts/password_change/password_reset_form.html'
    success_url = '/accounts/password_reset/done/'  # Change as needed

    def form_valid(self, form):
        # Call the parent form_valid method
        response = super().form_valid(form)
        # If the user exists (the email is valid), show a success message
        messages.success(self.request, "If an account with that email exists, a password reset email has been sent.")
        return response

    def form_invalid(self, form):
        # Optionally process form errors here
        return super().form_invalid(form)


class CustomPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'accounts/password_change/password_reset_done.html'


class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'accounts/password_change/password_reset_confirm.html'


class CustomPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'accounts/password_change/password_reset_complete.html'
