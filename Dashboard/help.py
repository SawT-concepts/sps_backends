from .models import *
from django.conf import settings
from django.core.mail import EmailMessage

'''HELPiNG FUNCTIONS'''
#update payment_history

#im trying to create this function here so when ever term is updated this would be fired if its session then it would be fired
def update_payment_status(school_id, term, session, term_changed_to):
    school = School.objects.get(id=school_id)
    term = term
    session = session
    new_term = term_changed_to

    students = Student.objects.filter(school=school)
    amount_in_debt = 0

    if session:
        for student in students:
            #think about first checking if the student was in debt then calculate the amount and add it
            # then calculate the amount and add it in total
            student.outstanding_amount = 0

            if student.payment_status == "OUTSTANDING" or student.payment_status == "IN DEBT" or student.is_outstanding == True:
                student.is_outstanding = True
                x = student.outstanding_amount
                amount_in_debt = student.amount_in_debt
                #exist here to create some variable to store student previous history if he was owing
                student.outstanding_amount = amount_in_debt + x

            current_class = student.grade
            next_grade = current_class.next_class_to_be_promoted_to

            #add a is promoted function here
            student.grade = next_grade
            student.payment_status == "IN DEBT"

            flat_fee = next_grade.first_term_school_fee

            if student.is_following_bus:
                bus_fee = next_grade.first_term_bus_fee
            else:
                bus_fee = 0

            if student.is_staying_in_hostel:
                hostel_fee = next_grade.first_term_hostel_fee
            else:
                hostel_fee = 0

            student.amount_in_debt == amount_in_debt + \
                bus_fee + flat_fee + amount_in_debt + hostel_fee + student.outstanding_amount
            student.save()

    elif term:
        for student in students:
            if student.payment_status == "OUTSTANDING" or student.payment_status == "IN DEBT":
                amount_in_debt = student.amount_in_debt

            current_class = student.grade
            student.payment_status == "IN DEBT"
            flat_fee = next_grade.first_term_school_fee

            if new_term == "FIRST TERM":
                if student.is_following_bus:
                    bus_fee = current_class.first_term_bus_fee
                else:
                    bus_fee = 0

                if student.is_staying_in_hostel:
                    hostel_fee = current_class.first_term_hostel_fee
                else:
                    hostel_fee = 0

                student.amount_in_debt == amount_in_debt + \
                    bus_fee + flat_fee + amount_in_debt + hostel_fee + student.outstanding_amount

            elif new_term == "SECOND TERM":
                if student.is_following_bus:
                    bus_fee = current_class.second_term_bus_fee
                else:
                    bus_fee = 0

                if student.is_staying_in_hostel:
                    hostel_fee = current_class.second_term_hostel_fee
                else:
                    hostel_fee = 0

                student.amount_in_debt == amount_in_debt + \
                    bus_fee + flat_fee + amount_in_debt + hostel_fee + student.outstanding_amount

            elif new_term == "THIRD TERM":
                if student.is_following_bus:
                    bus_fee = current_class.third_term_bus_fee
                else:
                    bus_fee = 0

                if student.is_staying_in_hostel:
                    hostel_fee = current_class.third_term_hostel_fee
                else:
                    hostel_fee = 0

                student.amount_in_debt == amount_in_debt + \
                    bus_fee + flat_fee + amount_in_debt + hostel_fee + student.outstanding_amount

            else:
                student.amount_in_debt = 0

            student.save()


#promote student class
'''HELPING FUNCTIONS END'''


def snd_email(title, template, send_to):
    email = EmailMessage(
        title,
        template,
        settings.EMAIL_HOST_USER,
        [send_to, ],
    )
    email.fail_silently = False
    email.send()


