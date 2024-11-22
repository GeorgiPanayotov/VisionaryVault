from django.urls import path

from VisionaryVaultApp.accounts import views
from VisionaryVaultApp.accounts.views import (CustomLogoutView,
                                              CustomLoginView,
                                              CustomChangePasswordView,
                                              CustomPasswordChangeDoneView,
                                              EmailChangeView, EmailChangeDoneView,
                                              CustomPasswordResetView,
                                              CustomPasswordResetConfirmView,
                                              CustomPasswordResetCompleteView,
                                              CustomPasswordResetDoneView)

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/delete/', views.delete_profile, name='delete_profile'),
    path('profile/details/', views.profile_details, name='profile_details'),
    path('profile/change-password/', CustomChangePasswordView.as_view(), name='change_password'),
    path('profile/change-password-done/', CustomPasswordChangeDoneView.as_view(), name='password_change_done'),
    path('change-email/', EmailChangeView.as_view(), name='change_email'),
    path('change-email-done/', EmailChangeDoneView.as_view(), name='email_change_done'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

