import os
from django.shortcuts import render, redirect
from django.contrib import messages
from Payments.models import payment
from .forms import Payment_form, Amount_form
from Dashboard.models import *
from .help import *

# importing the necessary libraries
from django.http import HttpResponse
from django.views.generic import View
from .process import html_to_pdf
from django.template.loader import render_to_string
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect
from .extra_functions import *
from django.template.loader import render_to_string
from Dashboard.help import snd_email

from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from .extra_functions import *
from django.contrib.sites.models import Site


'''
This view here i'm just creating it to see how it can capture the data from that form and render it
in the next fiew capturing the amount i would want to be paying
'''


def home_payment(request, school_id):

    # Add or initite a school id here so that it can be accessed in the display format
    school = School.objects.get(school_id=school_id)

    if request.method == 'POST':
        payment_form = Payment_form(request.POST)

        # validate the form
        if payment_form.is_valid():
            payment = payment_form.save(commit=False)

            # update model low key (DONE)
            ins = get_student(payment.registration_number, school.id)

            if ins == "Student does not exist":
                messages.error(request,
                               "A student with this registration number doesn't exist or this student hasn't been added to the school database!"
                               )
                payment_form = Payment_form(instance=payment)

                context = {
                    "form": payment_form,
                    "school": school
                }
                #
                return render(request, "payments/process_payment.html", context)
                # //send a return message (DONE)

            payment.student = ins

            z = payment.student
            # //payment.amount_to_be_paid = total_fees + debt_fee
            payment.amount_to_be_paid = z.amount_in_debt
            payment.school = school
            payment.academic_term = school.current_term
            payment.academic_session = school.academic_session
            payment.student_grade = z.grade
            if z.payment_status == "COMPLETED":
                school_id = z.id
                return redirect('no_pay', school_id)
            # // crete a no pay  function

            # // add redirect and an if here student payment status is settled s
            payment.save()
            pay = payment
            # run a redirect here to run the innput amount here
            return redirect('input amount', pay.payment_id)

        # // supposed to raise a form validation error here saying what happens if we can't find student

    # ? what happens if this isnt a post request
    else:

        payment_form = Payment_form()

        context = {
            "form": payment_form,
            "school": school,
        }

        ###############################################################
        return render(request, "payments/process_payment.html", context)


# ? Function here to show if student has paid completetly and is trying to make more payment
def no_pay(request, student_id):
    student = Student.objects.get(id=student_id)
    school = student.school

    context = {
        "student": student,
        "school": school,
    }
    if student.payment_status == "COMPLETED":
        return render(request, "payments/no_pay.html", context)
    else:
        return redirect('home_payment', school.school_school_id)


def input_amount(request, payment_id):

    #################################################
    p = get_payment(payment_id)

    if p == "invalid":
        return redirect('home_payment', payment_id)

    student = p.student  # pu it here to access if the sudent follows bus a
    current_term = p.school.current_term
    amount = p.amount_to_be_paid

    '''Boolcheck'''

    x = False
    y = False
    z = False

    if student.is_following_bus and student.is_in_hostel:
        x = True
        y = False
        z = False

    elif student.is_following_bus and student.is_in_hostel == False:
        x = False
        y = True
        z = False

    elif student.is_following_bus == False and student.is_in_hostel:
        x = False
        y = False
        z = True

    '''Boolcheck end'''

    if request.method == "POST":
        amount_form = request.POST['amount_paiid']

        if amount_form:
            amount = amount_form

            p.amount_paid = amount
            p.save()
            print("Success")
            return redirect('initiate_payment', payment_id)

            # return redirect ('initiate_payment', p.id)
        # work on error if its not valid

    else:
        payment_form = Amount_form()

    context = {

        "p": p,
        "school": p.school,
        "form": payment_form,
        "student": student,
        "current_term": current_term,
        "total_amount": amount,
        "both": x,
        "bus_only": y,
        "hostel_only": z,
    }
    #####################################################
    return render(request, "payments/input_amount.html", context)


def initiate_payment(request, payment_id):

    context = {}

    def get_payment(id):
        try:
            pay = payment.objects.get(payment_id=id)
            return pay
        except:
            pay = "invalid"
            return pay

    p = get_payment(payment_id)

    if p == "invalid":
        # work on this
        return redirect('home_payment', payment_id)

    student = p.student
    amount_paid = p.amount_paid
    total = (amount_paid + 500)

    hashed_value = process_hash(settings.PAYSTACK_PUBLIC_KEY, p.ref, total, p.email,
                                p.student.parent_phone_number, p.student.first_name, p.student.last_name)


    # todo Generate hash value here

    context = {

        "p": p,
        "school": p.school,
        "student": student,
        "total": total,
        "public_key": settings.PAYSTACK_PUBLIC_KEY
    }

    return render(request, "payments/initiate_payment.html", context)


def verify_payment(request, ref):
    paymentt = get_object_or_404(payment, ref=ref)
    verified = paymentt.verify_payment()
    current_site = Site.objects.get_current()

    if verified:
        # // process school fees, send email
        process_student_fees_status(paymentt)

        debt = int(paymentt.amount_to_be_paid) - int(paymentt.amount_paid)

        # ?EMAIL
        data = {
            "student": paymentt.student,
            "payment": paymentt,
            "site": current_site,
            "debt": debt
        }

        title = f'Payment Notification from {paymentt.school.name}'
        email = paymentt.student.parent_email
        templte = render_to_string('emails/information.html', data)
        snd_email(title, templte, email)
        # ? EMAIL END

        title_2 = f'Payment Notification from {paymentt.school.name}'
        email_2 = paymentt.email
        templte_2 = render_to_string('emails/payer.html', data)
        snd_email(title_2, templte_2, email_2)

        # // TODO MAKE PAYMENT DATE PAID HERE
        gernerate_qr(paymentt.payment_id)
        return redirect('success', paymentt.id)

    else:
        # // TODO redirect to faiure page
        print("unverif")


def success_payment(request, payment_id):
    # todo ADD SECURITY VERIFICATION HERE
    paymentt = get_object_or_404(payment, id=payment_id)
    student = paymentt.student
    school = paymentt.school

    context = {
        "student": student,
        "school": school,
        "payment": paymentt
    }

    return render(request, "payments/success_payment.html", context)


# # ///todo add a date paid to the payment model
# class GeneratePdf(View):

#     def get(self, request, *args, **kwargs):

#         pay = get_payment(kwargs['payment_id'])

#         if pay == "invalid":
#             return pay
#             # todo return a cool redirect here

#         # //pass pay here as a variable for the context

#         with open('temp.html', 'w') as f:
#             f.write(render_to_string('result.html', {'data': pay}))


#         # Converting the HTML template into a PDF file
#         pdf = html_to_pdf('temp.html')

#         # rendering the template
#         return HttpResponse(pdf, content_type='application/pdf')


def render_pdf_view(request, payment_id):

    pay = get_payment(payment_id)

    if pay == "invalid":
        return pay
    debt = pay.amount_to_be_paid - pay.amount_paid
    template_path = 'result.html'
    context = {'data': pay, "debt": debt}

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


# ? VIEW FUNCTION TO VERIFY THE PAYMENT THAT IS BEING MADE HERE
def verify_reciept(request, payment_id):

    pay = get_payment(payment_id)

    if pay == "invalid":
        return pay
        # TODO redirect here

    context = {
        "payment": pay,
        "school": pay.school
    }

    return render(request, "payments/verified.html", context)
