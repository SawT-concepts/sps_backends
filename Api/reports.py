# here i would work on some stuffs that takes a
from dataclasses import dataclass
from decimal import Decimal
from Payments.models import *
from Dashboard.models import *
from django.db.models import Sum
from django.db.models.functions import TruncDay
from django.utils import timezone
from datetime import  timedelta


@dataclass
class report_entry:
    school: School
    amount_paid: Decimal
    students_paid: int
    students_not_paid: int
    total_students: int
#add budget in amount here
    school_budget: Decimal
    real_budget: Decimal

@dataclass
class student_entry:
    students_paid: int
    students_outstanding: int
    students_in_debt: int
    total_students: int

@dataclass
class bar_graph:
    day: str
    total_amount: int



#? work on this so it won't be spitting out only one report entry
def process_report(school_id):
    data = []
    p_instance = payment.objects.select_related('school').filter(is_active=True, school = school_id).values("school").annotate(
        amount_paid=Sum("amount_paid")
    )

    if p_instance:
        ins = list(p_instance)
    else:
        ins = [{'school': school_id, 'amount_paid': 0.00}]

    total = Student.objects.select_related('school').filter(school=school_id).count()
    students_paid = Student.objects.select_related('school').filter(
        school=school_id, payment_status="COMPLETED").count()
    student_not_paid = total - students_paid
    school = School.objects.get(id=school_id)
    bud = school.budget



    for entry in ins:
        school = School.objects.get(pk=(entry["school"]))
        per = (entry["amount_paid"]/bud) * 100
        rep = report_entry(
            school, entry["amount_paid"],  students_paid, student_not_paid, total, per, bud)
        data.append(rep)

    return data



#? FOR GETTING STUDENT
def get_student_payment_graph(id):
    data = []


    students_paid = Student.objects.select_related('grade').filter(
        grade=id, payment_status="COMPLETED").count()
    students_outstanding = Student.objects.select_related('grade').filter(
        grade=id, payment_status="OUTSTANDING").count()
    students_in_debt = Student.objects.select_related('grade').filter(
        grade=id, payment_status="IN DEBT").count()
    total = students_paid + students_outstanding + students_in_debt

    x = student_entry(students_paid, students_outstanding, students_in_debt, total)

    data.append(x)

    return data

#for the bar graph in the dashboard
def get_week_payment_graph (school_id):

    data = []
    new_date = timezone.now().date() - timedelta(days=7)
    p_instance = payment.objects.select_related('school').filter(
            is_active=True,
            school=school_id,
            date_paid__gte= new_date
        ).values(
            day = TruncDay('date_paid'),
        ).annotate(
            total_amount=Sum('amount_paid')
        )


    for i in p_instance:
        day = i['day'].strftime("%A")
        total_amount = i['total_amount']

        entry = bar_graph(day, total_amount)
        data.append(entry)

    return data

