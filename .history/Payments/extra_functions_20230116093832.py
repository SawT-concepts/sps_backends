
# ? FUNCTION TO UPDATE THE STUDENT PAYMENT STATUS AFTER HE HAS PAID
import hashlib


def process_student_fees_status(paymentt):
    student = paymentt.student
    amount_paid = paymentt.amount_paid
    amount_in_debt = student.amount_in_debt
    updated_amount = amount_in_debt - amount_paid
    outstanding_fix = student.outstanding_amount - amount_paid

    student.amount_in_debt = updated_amount

    if outstanding_fix <= 0:
        student.outstanding_amount = 0
        student.is_outstanding = False
        student.payment_status = "IN DEBT"
    else:
        student.outstanding_amount = outstanding_fix

    if updated_amount <= 0:
        student.payment_status = "COMPLETED"

    student.save()


def process_hash(public_key, ref, amount, email, phone_number, first_name, last_name, processed_url):
    x = [
        "publicKey",
        'amount',
        'callbackUrl',
        'country',
        'currency',
        'email',
        'firstName',
        'lastName',
        'phoneNumber',
        'transactionId'
    ]

    body = {
        "publicKey": public_key,
        "transactionId": ref,
        "amount": str(amount),
        "currency": "NGN",
        "country": "NG",
        "email": email,
        "phoneNumber": phone_number,
        "firstName": first_name,
        "lastName": last_name,
        "callbackUrl": processed_url
    }

    hashed_value = ""
    for index in x:
        new = body.get(index)
        hashed_value += new

    print(hashed_value)
    hashed_string = hashlib.sha256(hashed_value.encode('utf-8')).hexdigest()

    retu(hashed_string)
