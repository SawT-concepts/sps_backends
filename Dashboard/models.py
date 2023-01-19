from django.db import models
from shortuuid.django_fields import ShortUUIDField

# Create your models here.

class School (models.Model):

    academic = (
    ("2019/2020", "2019/2020"),
    ("2020/2021", "2020/2021"),
    ("2021/2022", "2021/2022"),
    ("2022/2023", "2022/2023"),
    ("2023/2024", "2023/2024"),
    ("2024/2025", "2024/2025"),
    )

    school_terms = (
    ("FIRST TERM", "FIRST TERM"),
    ("SECOND TERM", "SECOND TERM"),
    ("THIRD TERM", "THIRD TERM"),
    )


    name = models.CharField(max_length=200, blank=False, null=False)
    school_address = models.TextField()
    logo = models.ImageField(max_length=70,  upload_to="Profiles",  blank = True)
    school_background = models.ImageField ( upload_to= "School Background", blank = True,)
    email = models.EmailField( max_length=254)
    budget = models.BigIntegerField(null=True)
    mobile_number = models.CharField( max_length=50)
    #? Added school passwords for admin verification
    school_password = models.CharField( max_length=10, null=True, blank=False)

    #here just to check if adding a list of hex codes would work here
    brand_color = models.CharField( max_length=50)
    accent_color = models.CharField(max_length=50)

    academic_session = models.CharField( choices=academic, max_length=50)
    current_term = models.CharField(choices=school_terms, max_length=50)

    account_number = models.BigIntegerField()
    school_id= ShortUUIDField( length = 9,
        max_length = 9, unique = True)


    def __str__(self):
        return self.name

    def save  (self, *args, **kwargs):
        if not self.pk:
            print ("already saved")
        super().save(*args, **kwargs)


    #add a pre-save method here so this form here would be able to ccreate a "Graduted class for the school"

class Grade (models.Model):
    name = models.CharField( max_length=50)
    school = models.ForeignKey("Dashboard.School", on_delete=models.CASCADE)
    first_term_school_fee = models.BigIntegerField(default=0, blank=True)
    first_term_hostel_fee = models.BigIntegerField(default=0, blank=True)
    first_term_bus_fee = models.BigIntegerField(default=0, blank=True)
    second_term_school_fee = models.BigIntegerField(default=0, blank=True)
    second_term_hostel_fee = models.BigIntegerField(default=0, blank=True)
    second_term_bus_fee = models.BigIntegerField(default=0, blank=True)
    third_term_school_fee = models.BigIntegerField(default=0, blank=True)
    third_term_hostel_fee = models.BigIntegerField(default=0, blank=True)
    third_term_bus_fee = models.BigIntegerField(default=0, blank=True)

    #check this on stackoverflow
    next_class_to_be_promoted_to = models.ForeignKey("Dashboard.grade",
                                                    on_delete=models.CASCADE,
                                                    blank= True,
                                                    null= True
                                                    )
    grade_id = ShortUUIDField(editable=False, length=9,
                               max_length=9, unique=True)

    class Meta:
        verbose_name = ("Class")
        verbose_name_plural = ("Classes")

    def __str__(self):
        return self.name



class Student (models.Model):
    payment_stats = (
        ("COMPLETED", "COMPLETED"),
        ("OUTSTANDING", "OUTSTANDING"),
        ("IN DEBT", "IN DEBT")
    )

    first_name = models.CharField( max_length=50)
    middle_name = models.CharField(max_length=50, blank=True,)
    last_name = models.CharField( max_length=50)
    registration_number = models.CharField(max_length=200, unique=True)
    parent_email = models.EmailField(
        ("parent's email"), max_length=254, blank=True,)
    parent_phone_number = models.CharField(max_length=50, blank=True,)
    school = models.ForeignKey("Dashboard.School", on_delete=models.CASCADE, blank = True,)
    grade = models.ForeignKey(
        "Dashboard.grade", on_delete=models.CASCADE, blank=True,)
    is_following_bus = models.BooleanField(default=False)
    is_in_hostel = models.BooleanField(default=False)
    payment_status = models.CharField(choices= payment_stats, max_length=50, default="IN DEBT")
    #HOPERFULLY THE ADDITION OF THE CURRENT SCHOOL FEES AND THE OUTSTANDING AMOUNT
    amount_in_debt = models.BigIntegerField(default=0)

    #function here to check if student is having any outstanding payment
    is_outstanding = models.BooleanField(default=False)
    outstanding_amount = models.BigIntegerField(default=0)


    def __str__(self):
        return self.first_name

