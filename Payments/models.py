import datetime
from django.db import models
from shortuuid.django_fields import ShortUUIDField
from .paystack import PayStack
from Dashboard.models import Student
import string
import random
from .remita import Remita


# Create your models here.
class payment(models.Model):
    def get_deleted_user_instance():
        return Student.objects.get(first_name='Deleted')

    registration_number = models.CharField(
        max_length=50, blank=False, null=True)
    email = models.EmailField(max_length=254, blank=True, null=True)
    student_grade = models.CharField(null=True, max_length=50)

    academic_session = models.CharField(max_length=50)
    academic_term = models.CharField(max_length=50)
    amount_paid = models.BigIntegerField(blank=True, null=True)

    # would addd this when instanciating the payment
    amount_to_be_paid = models.BigIntegerField(blank=True, null=True)
    date_paid = models.DateTimeField(blank=True, null=True)
    student = models.ForeignKey(
        "Dashboard.Student", on_delete=models.SET(get_deleted_user_instance), blank=True, null=True)
    school = models.ForeignKey(
        "Dashboard.School", on_delete=models.SET_NULL, blank=True, null=True)
    amount_in_debt = models.BigIntegerField(blank=True, null=True)
    # would also try and sort things out by date proccesed

    # add payment status here so that filtering would wprk ON THE PAYMENT RECIEPT
    has_been_processed = models.BooleanField(default=False)

    # PAYMENT STATUS ON THE GRAPH
    is_active = models.BooleanField(default=False)
    payment_id = ShortUUIDField(editable=False, length=9,
                                max_length=9, unique=True)
    image = models.ImageField(upload_to="reciepts", null=True)
    hash = models.CharField(max_length=100, null=True, blank=True)

    # payment info
    ref = models.CharField(max_length=100)

    def __str__(self):
        return self.payment_id

    def save(self, *args, **kwargs):

        while not self.ref:
            letters = string.ascii_lowercase
            ref = (''.join(random.choice(letters) for i in range(10)))
            object_with_similar_ref = payment.objects.filter(ref=ref)
            if not object_with_similar_ref:
                self.ref = ref
        super().save(*args, **kwargs)


    # this function heere is supposed to check  forr verification if it return true it means the ref is verified
    def verify_payment(self):
        pay = Remita()
        result, status= pay.verify_payment(self.ref)

        # if it has a good connection with the api then this runs
        if status:
            print(
                'There is a status interpretation here and its showing that we have a status report 200')

            print(result['amount'])

            if result['amount'] == (self.amount_paid):
                # here is just going to verify if thee prices match
                self.is_active = True
                self.has_been_processed = True
                self.date_paid = datetime.datetime.now()
                self.save()

        if self.is_active:
            return True

        return False
