from django.contrib import admin
from django.urls import path, include
from board_data import views
from django.contrib.auth import views as auth_views
from accounts import views as accounts_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('board_data.urls')),
    path('', include('accounts.urls')),
    path('settings/account/', accounts_views.UserUpdateView.as_view(), name='my_account'),


    
    path('reset/', auth_views.PasswordResetView.as_view(
        template_name = 'password_reset.html',
        email_template_name = 'password_reset_email.html',
        subject_template_name = 'password_reset_subject.txt'
    ), name='password_reset'),

    path('reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name = 'password_reset_done.html'
    ), name= 'password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name = 'password_reset_confirm.html'
    ), name = 'password_reset_confirm'),

    path('reset/complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name = 'password_reset_complete.html'
    ), name = 'password_reset_complete'),

    path('settings/password/', auth_views.PasswordChangeView.as_view(
        template_name = 'password_change.html'
    ), name='password_change'),
    
    path('settings/passwword/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='password_change_done.html'), name='password_change_done'),
]
