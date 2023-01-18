from django.db.models.query_utils import Q
from .forms import PasswordResetForm
from django.shortcuts import  render, redirect
from .forms import NewUserForm
from django.contrib import messages
from .models import profile
from django.contrib.auth.models import User
from .forms import PasswordResetForm, EditUserProfile
from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from Dashboard.help import snd_email



def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if request.FILES:
            print("yes fi;es")

        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()
            return redirect("edit-account", user.id)
        messages.error(request, form.errors)
    form = NewUserForm()
    return render (request=request, template_name="s-admin/register.html", context={"register_form":form})



def edit_account (request, user_id):
    account = profile.objects.get(user=user_id)
    if request.method == "POST":
        form = EditUserProfile(request.POST, request.FILES, instance=account)
        if form.is_valid():
            profyl = form.save()
            profyl.save()
        messages.error (request, form.errors )
    form = EditUserProfile(instance=account)
    return render (request, "s-admin/edit_profile.html", context={"form":form})


