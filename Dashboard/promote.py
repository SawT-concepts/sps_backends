from Dashboard.models import Student
from Payments.models import payment
def promote (x_students, school):
    promoted = Student.objects.filter(school=school)
    print(x_students)

    for learners in promoted:
        if learners.id in x_students:
            print("this guy didn't promote")
        else:

            grade = learners.grade
            new_grade = grade.next_class_to_be_promoted_to

            learners.grade = new_grade
            learners.save()


def refresh_payment (school):
    pay = payment.objects.filter(school=school)

    for x in pay:
        x.is_active = False
        x.save()