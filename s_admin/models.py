from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver



#add blank false here
class profile(models.Model):
    school = models.ForeignKey("Dashboard.School", on_delete=models.CASCADE, null=True)
    profile_pic = models.ImageField(max_length=70,  upload_to="Profiles",  null=True)
    phone_number = models.CharField( max_length=50, null=True)
    security_key = models.CharField(max_length=30, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        print("here")
        u = profile.objects.create(user=instance)
        u.save()


