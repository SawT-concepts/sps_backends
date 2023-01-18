
#? FUNCTION TO UPDATE THE STUDENT PAYMENT STATUS AFTER HE HAS PAID
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
