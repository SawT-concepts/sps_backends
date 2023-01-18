from django.contrib.auth.forms import PasswordResetForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import SetPasswordForm
from s_admin.models import profile


# Create your forms here.

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("first_name", "last_name", "username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user

class EditUserProfile (forms.ModelForm):
	class Meta:
		model = profile
		fields = ("school", "profile_pic", "phone_number", "security_key")


class PasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)



# class SetPasswordForm(SetPasswordForm):
#     class Meta:
#         model = User
#         fields = ['new_password1', 'new_password2']
