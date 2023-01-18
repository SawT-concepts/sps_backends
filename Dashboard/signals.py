from re import U
from django.db.models.signals import post_save
from .models import School
from django.dispatch import receiver
from .models import Grade



def create_grade_on_school_created(sender, instance, created, **kwargs):
    if created:
        print("here")
        u = Grade.objects.create(school=instance, name="Graduated")
        u.save()
        u.next_class_to_be_promoted_to = u 
        print("here2")
        u.save()


post_save.connect(create_grade_on_school_created, sender=School)


#// Firing even when school object os updated