from Dashboard.models import *
from Payments.models import *
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
import random
from Dashboard.models import Grade


# get student by id....


def get_student(registration_number, school_id):
    try:
        reply = Student.objects.get(
            registration_number=registration_number, school=school_id)
        return reply
    except:
        reply = "Student does not exist"
        return reply

    # validation to check the paymen


def get_payment(id):
    try:
        pay = payment.objects.get(payment_id=id)
        return pay
    except:
        pay = "invalid"
        return pay


def generate_fees(school, is_in_hostel, is_following_bus, grade_id):
    current_term = school.current_term
    print(grade_id.id)
    u = grade_id.id
    grade = Grade.objects.get(id=u)

    if current_term == "FIRST TERM":
        if is_in_hostel:
            x = grade.first_term_hostel_fee
        else:
            x = 0

        if is_following_bus:
            y = grade.first_term_bus_fee
        else:
            y = 0

        total = x + y + grade.first_term_school_fee

    elif current_term == "SECOND TERM":
        if is_in_hostel:
            x = grade.second_term_hostel_fee
        else:
            x = 0

        if is_following_bus:
            y = grade.second_term_bus_fee
        else:
            y = 0

        total = x + y + grade.second_term_school_fee

    elif current_term == "THIRD TERM":
        if is_in_hostel:
            x = grade.third_term_hostel_fee
        else:
            x = 0

        if is_following_bus:
            y = grade.third_term_bus_fee
        else:
            y = 0

        total = x + y + grade.third_term_school_fee

    return total


def gernerate_qr(id):
    pay = get_payment(id)

    pay
    link = "https://myspsonline.com" + \
        '/' + 'payment/verify-reciept' + '/' + pay.payment_id
    print(link)

    ####################
    qrcode_img = qrcode.make(link)
    canvas = Image.new("RGB", (800, 800), "white")
    draw = ImageDraw.Draw(canvas)
    canvas.paste(qrcode_img)
    buffer = BytesIO()
    canvas.save(buffer, "PNG")
    print("rached the pt")
    pay.image.save(f'image{random.randint(0,9999)}',
                   File(buffer))
    canvas.close()

