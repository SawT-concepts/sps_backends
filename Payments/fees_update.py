from Dashboard.models import School, Student
from django.template.loader import render_to_string
from Dashboard.help import snd_email

def session_update(student, school):
    '''important variables'''

    school = School.objects.get (id=school)
    student = Student.objects.get(id=student)

    x = school.current_term  # variable used to get student's term
    y = student.grade  # variable used to get studenr's grade
    z = student  # variable used get student's data

    # validation for first term
    if x == "FIRST TERM":
        school_fee = y.first_term_school_fee
        if z.is_in_hostel:
            hostel_fee = y.first_term_hostel_fee
        else:
            hostel_fee = 0

        if z.is_following_bus:
            bus_fee = y.first_term_bus_fee
        else:
            bus_fee = 0

        total_fees = school_fee + hostel_fee + bus_fee



    # validation for second term fees
    elif x == "SECOND TERM":
        school_fee = y.second_term_school_fee

        if z.is_in_hostel:
            hostel_fee = y.second_term_hostel_fee
        else:
            hostel_fee = 0

        if z.is_following_bus:
            bus_fee = y.second_term_bus_fee
        else:
            bus_fee = 0

        total_fees = school_fee + hostel_fee + bus_fee

 

    # validation for third term fees
    elif x == "THIRD TERM":
        school_fee = y.third_term_school_fee

        if z.is_in_hostel:
            hostel_fee = y.third_term_hostel_fee
        else:
            hostel_fee = 0

        if z.is_following_bus:
            bus_fee = y.third_term_bus_fee
        else:
            bus_fee = 0

        total_fees = school_fee + hostel_fee + bus_fee
        

    # validation for no fees at all
    else:
        print("No fees available..... some error happened")
    
    z.outstanding_amount = z.amount_in_debt

    z.amount_in_debt = z.outstanding_amount + total_fees

    if z.outstanding_amount > 0:
        z.payment_status = "OUTSTANDING"
        z.is_outstanding = True
    else:
        z.payment_status = "IN DEBT"
    z.save()

    #? Email send to the student
    title = f'New Term Fees Notification from {z.school.name}'
    data = {
        "student": z,
        "school": z.school
    }

    templte = render_to_string('emails/update.html', data)

    email = z.parent_email

    snd_email(title, templte, email)



#?promote student before you change school info

