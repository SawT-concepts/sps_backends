from cProfile import Profile
from django.contrib import admin
from .models import *
from django.contrib import admin
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin


class UserProfileInline(admin.StackedInline):
 model = profile
 max_num = 1
 can_delete = False


class UserAdmin(AuthUserAdmin):
 inlines = [UserProfileInline]


# unregister old user admin
admin.site.unregister(User)
# register new user admin
admin.site.register(User, UserAdmin)
