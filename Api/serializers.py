from dataclasses import fields
from Configuration.models import *
from Dashboard.models import School, Student, Grade
from Payments.models import payment
from rest_framework import serializers
from django.contrib.auth.models import User
from s_admin.models import profile

# Tutourial serializer

# ? Serializer that checks the tutorial page
class Tutorial_generalserializer(serializers.ModelSerializer):
    class Meta:
        model = Tutorial
        fields = ("__all__")

    # table = serializers.PrimaryKeyRelatedField(
    # queryset=Table.objects.filter(is_active=True))

# gets the basic information about the users name

# ? Serializr that displays the users info
class User_Serializer (serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")


# gets additional info about the users profile
class User_profile_serializer (serializers.ModelSerializer):
    user = User_Serializer()

    class Meta:
        model = profile
        fields = ("profile_pic", "user")


# get school info
class school_short_info_serializer (serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ("id", "name", "academic_session", "current_term", "logo")


class student_serializer (serializers.ModelSerializer):
    #just remebered that i need to edit the date paid instance after payment confirmend
    class Meta:
        model = Student
        fields = ("first_name", "last_name", "registration_number", )


# latest payment update
class latest_payment_serializer (serializers.ModelSerializer):
    student = student_serializer()

    class Meta:
        model = payment
        fields = ("id", "student", "payment_id", "amount_paid", "email",
                  "academic_session", "academic_term", "date_paid")

# together
class school_serializer (serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ("name",)


class Support_serializer(serializers.ModelSerializer):
    class Meta:
        model = Support_Message
        fields = ("title", "body", "school")
# together
class report_entry_serializer (serializers.Serializer):
    school = school_serializer()
    amount_paid = serializers.DecimalField(max_digits=15, decimal_places=2)
    students_paid = serializers.IntegerField()
    students_not_paid = serializers.IntegerField()
    total_students = serializers.IntegerField()
    school_budget = serializers.DecimalField(max_digits=15, decimal_places=1)
    real_budget = serializers.DecimalField(max_digits=15, decimal_places=2)


class bar_graph_serializer (serializers.Serializer):
    day = serializers.CharField()
    total_amount = serializers.IntegerField()



# GRADE SECTION
class student_graph_entry_serializer (serializers.Serializer):
    students_paid = serializers.IntegerField()
    students_outstanding = serializers.IntegerField()
    students_in_debt = serializers.IntegerField()
    total_students = serializers.IntegerField()


class nxt_grade_serializer (serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = ("name",'id')


class test_serializer((serializers.PrimaryKeyRelatedField)):
    def get_queryset(self):
        user = self.context['request'].user
        prof = profile.objects.get(user=user)
        school = prof.school
        queryset = Grade.objects.filter(school=school)
        return queryset


class grade_write_serializer (serializers.ModelSerializer):
    next_class_to_be_promoted_to = test_serializer()
    class Meta:
        model = Grade
        fields = ("id", "name", "first_term_school_fee",
                  "first_term_hostel_fee", "first_term_bus_fee",
                  "second_term_school_fee", "second_term_hostel_fee",
                  "second_term_bus_fee", "third_term_school_fee",
                  "third_term_hostel_fee", "third_term_bus_fee",
                  "next_class_to_be_promoted_to")


class grade_read_serializer (serializers.ModelSerializer):
    next_class_to_be_promoted_to = nxt_grade_serializer()
    class Meta:
        model = Grade
        fields = ("id", "name", "first_term_school_fee",
                  "first_term_hostel_fee", "first_term_bus_fee",
                  "second_term_school_fee", "second_term_hostel_fee",
                  "second_term_bus_fee", "third_term_school_fee",
                  "third_term_hostel_fee", "third_term_bus_fee",
                  "next_class_to_be_promoted_to")




class student_short_serializer (serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ("id", "first_name", "last_name", "registration_number", "parent_email", "parent_phone_number",
                    "payment_status", "is_following_bus", "is_in_hostel", "amount_in_debt")



class read_student_serializer (serializers.ModelSerializer):
    grade = nxt_grade_serializer()
    class Meta:
        model = Student
        fields = ("id","first_name", "last_name", "registration_number", "parent_email",
                  "parent_phone_number", "payment_status", "amount_in_debt", "outstanding_amount", "is_following_bus", "is_in_hostel", "grade")


class write_student_serializer (serializers.ModelSerializer):
    grade = test_serializer()

    class Meta:
        model = Student
        fields = ("id", "first_name", "last_name", "registration_number", "parent_email",
                  "parent_phone_number", "is_following_bus", "is_in_hostel", "grade")




class Full_school_serializer (serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ("__all__")


class x_serializer (serializers.Serializer):
    id = serializers.IntegerField()
    first_name = serializers.CharField()




class Promotion_serializer (serializers.Serializer):
    student = x_serializer(many=True)


class user_list_serializers (serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("__all__")



class profile_serial (serializers.ModelSerializer):
    user = user_list_serializers()
    class Meta:
        model = profile
        fields = ("__all__")