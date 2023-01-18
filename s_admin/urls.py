from django.urls import path
from .views import *
from . import views
from django.contrib.auth import views as auth_views

#create account
#forgotten password
urlpatterns = [
    path("register", views.register_request, name="register"),
    path('edit-s-admin/<str:user_id>', views.edit_account, name="edit-account"),



    path ('reset_password', auth_views.PasswordResetView.as_view(
        template_name="s-admin/password_reset.html"
    ), name="reset_password"),

    path ('reset_password_sent', auth_views.PasswordResetDoneView.as_view(
        template_name="s-admin/password_reset_done.html"
    ), name="password_reset_done"),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name="s-admin/password_reset_confirm.html"), name='password_reset_confirm'),


    path('reset_password_complete', auth_views.PasswordResetCompleteView.as_view(
        template_name='s-admin/password_reset_complete.html'), name='password_reset_complete'),

]
