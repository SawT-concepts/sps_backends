from rest_framework.generics import GenericAPIView
from django.shortcuts import render
from rest_framework import generics
from Configuration.models import *
from .serializers import *
from s_admin.models import profile
from rest_framework import filters, status
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .reports import process_report, get_student_payment_graph, get_week_payment_graph
from rest_framework.viewsets import ModelViewSet
from Payments.fees_update import session_update
from Payments.help import generate_fees
from Dashboard.promote import promote, refresh_payment
from django_filters.rest_framework import DjangoFilterBackend
from django.template.loader import render_to_string
from Dashboard.help import snd_email


# Login view
class LoginView(APIView):
    permission_classes = ()

    def post(self, request,):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)

        if user:
            return Response({"token": user.auth_token.key})
        else:
            return Response({"error": "Wrong login Information. Please check your username and password and try again"}, status=status.HTTP_400_BAD_REQUEST)


#? EVERYPAGE (NAVIGATION)
# view to get user profile to display in the navigation section
class get_user_profile (generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        prof = profile.objects.filter(user=user)
        return prof

    serializer_class = User_profile_serializer

#? EVERYPAGE (NAVIGATION)
# the end point that connects or show all the details of the school
class get_short_school_info (APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        prof = profile.objects.get(user=user)
        school = prof.school
        s = school_short_info_serializer(school)

        print(s.data)
        return Response(s.data,  status=status.HTTP_200_OK)

    # serializer_class = school_short_info_serializer

#? EVERYPAGE (NAVIGATION)
# Get List of tutourials
class Tutorial_listapiview (generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Tutorial.objects.all()
    serializer_class = Tutorial_generalserializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', ]


#? DASHBOARD PAGE
# for the table in the dashboard page
class latest_payments (generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = latest_payment_serializer

    def get_queryset(self):
        user = self.request.user
        prof = profile.objects.get(user=user)
        school = prof.school

        # add order by in the payment model
        pay = payment.objects.filter(
            school=school, is_active=True).order_by("-date_paid")[:60]
            #!FIX LATER

        return pay


#? FOR THE GRAPH IN THE DASHBOARD PAGE
#// todo would need to rearrange the modelling here so that it can return a data representation of the class when empty
class report_entry_view (APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = self.request.user
        prof = profile.objects.get(user=user)
        school = prof.school.id

        data = process_report(school)
        serializer = report_entry_serializer(instance=data, many=True)
        return Response(data=serializer.data)

class bar_graph_view (APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = self.request.user
        prof = profile.objects.get(user=user)
        school = prof.school.id

        data = get_week_payment_graph(school)
        serializer = bar_graph_serializer(instance=data, many=True)
        return Response(data=serializer.data)


class students_graph (APIView):

    permission_classes = [IsAuthenticated]
    def get(self, request, grade):
        user = self.request.user
        prof = profile.objects.get(user=user)
        school = prof.school

        data = get_student_payment_graph(grade)
        serializer = student_graph_entry_serializer(instance=data, many=True)
        return Response(data=serializer.data)


#? THE VIEW THAT CREATES AN ENDPOINT TO SEE, DELETE AND EDIT A CLASS
#// todo (work on the section in the models that deletes a student's class instance after the class deletes)
class grade_view (ModelViewSet):
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', ]


    def get_serializer_class (self):
        if self.action in ("list", "retrieve"):
            return grade_read_serializer
        return grade_write_serializer

    def get_queryset(self):
        user = self.request.user
        prof = profile.objects.get(user=user)
        school = prof.school
        grades = Grade.objects.select_related('school').filter (school=school).order_by("-id")
        return grades


    def get_serializer_context(self):
        return {'request': self.request}


    def perform_create(self, serializer):
        user = self.request.user
        prof = profile.objects.get(user=user)
        school = prof.school
        #! add a serializer validation here
        serializer.is_valid(raise_exception=True)
        serializer.save( school=school)


#? get students based on class [CLASS PAGE]
# // work on the serializer class here to remove payment status on adding of student
class get_student_bcAPI (GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = student_short_serializer


    def get_queryset(self):
        u = Student.objects.select_related('grade').filter (grade= self.kwargs['grade'])
        print (u)
        return u

    filter_backends = [filters.SearchFilter, ]
    search_fields = ('first_name',)


    def get(self, request, grade):
        #! Add a check for grade fulter here
        students = Student.objects.filter(grade=grade)
        data = students
        serializer = student_short_serializer(data, many=True)
        return Response(data=serializer.data)


    def post (self, request, grade):
            user = self.request.user
            prof = profile.objects.get(user=user)
            school = prof.school
            gd = Grade.objects.get(id=grade)
            #! add a serializer validation here
            serializer = student_short_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            total_fees = generate_fees(school, serializer.validated_data.get('is_in_hostel'), serializer.validated_data.get('is_following_bus'), gd)
            serializer.save( grade=gd, school=school, amount_in_debt=total_fees)
            return Response(status=status.HTTP_201_CREATED)



#? STUDENT PAGE
# the end point that shows the list of all the studdents
# // PERFORM Create has to be here
# // Implement the Write serializer
class view_student (ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = read_student_serializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['registration_number', 'first_name', 'last_name']
    filterset_fields = {'grade': ['exact'],
                        'payment_status': ['exact'],
                        'is_outstanding': ['exact'],
                        'outstanding_amount': ['gt', 'lt'],
                        'amount_in_debt': ['gt', 'lt'], }



    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return read_student_serializer
        return write_student_serializer

    def get_queryset(self):
        user = self.request.user
        prof = profile.objects.get(user=user)
        school = prof.school
        students = Student.objects.select_related('school').filter(school=school)
        return students

    def perform_create(self, serializer):
        user = self.request.user
        prof = profile.objects.get(user=user)
        school = prof.school
        serializer.is_valid(raise_exception=True)
        total_fees = generate_fees(school, serializer.validated_data.get('is_in_hostel'), serializer.validated_data.get('is_following_bus'), serializer.validated_data.get('grade') )
        #! add a serializer validation here
        serializer.save( school=school, amount_in_debt=total_fees)



# ? GET LIST OF THE STUDENT PAYMENT HISTORY
# // todo Get student payment history
class payment_history (generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = latest_payment_serializer


    def get_queryset(self):
        stud = Student.objects.get(id=self.kwargs['student'])
        p = payment.objects.select_related('student').filter (student=stud, has_been_processed=True)
        # todo Add order by date here
        return p


#? School edit view
class school_view (ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = Full_school_serializer
    queryset = School.objects.all()

    def perform_update(self, serializer,):
        #// todo Add a logic here that checks the changes and fire the function to alter studentd
        #// todo If save the initial school term and session
        prev = School.objects.get (id = self.kwargs['pk'])
        prev_academic_session = prev.academic_session
        prev_current_term = prev.current_term
        serializer.save()
        # // ! check of the previous term and session has changed
        # get all the student for that school
        new = School.objects.get(id=self.kwargs['pk'])
        current_academic_session = new.academic_session
        current_current_term = new.current_term

        print (current_current_term)
        print (prev_current_term)
        print(prev_academic_session)
        print(current_academic_session)

        if prev_academic_session != current_academic_session or prev_current_term != current_current_term:
            school_id = prev.id
            students = Student.objects.select_related('school').filter(school=school_id)

            refresh_payment (school_id)

            for student in students:
                session_update(student.id, school_id)


#? Promote Students
class Promote_students (APIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        prof = profile.objects.get(user=user)
        school = prof.school
        return Student.objects.filter(school=school)


    def post (self, request,):
        serializer = Promotion_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        failed_students = serializer.validated_data.get('student')

        x_students = []

        for students in failed_students:
            x = str(students['id'])
            x_students.append(x)

        user = self.request.user
        prof = profile.objects.get(user=user)
        school = prof.school

        promote (x_students, school.id)
        print ("babe")
        return Response("SUCCESSFUL", status=status.HTTP_200_OK)



#//\todo this component here is what is going to be responsible when admin hits the end point for remind parents
#? Remind parents
class Remind_students (APIView):
    permission_classes = [IsAuthenticated]


    def post (self, request):
        serializer = Promotion_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        debt_students = serializer.validated_data.get('student')
        ################
        user = self.request.user
        prof = profile.objects.get(user=user)
        school = prof.school

        title = f'Payment OverDue Notification from {school.name}'

        ################
        x_students = []


        for students in debt_students:
            print("processed students")
            x = str(students['id'])
            x_students.append(x)

        for student in x_students:

            data = {
                "student": Student.objects.get(id=student)
            }

            ex = Student.objects.get(id=student)
            templte = render_to_string('emails/remind.html', data)
            email = ex.parent_email
            # todo add section for wrong email verification
            snd_email(title, templte, email)

        return Response("SUCCESSFUL", status=status.HTTP_200_OK)



class profile_view (ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = profile_serial

    def get_queryset (self):
        user = self.request.user
        prof = profile.objects.get(user=user)
        school = prof.school
        return profile.objects.filter(school=school)

    def perform_update (self, serializer):
        prev = profile.objects.get (id = self.kwargs['pk'])

        prev_profile_condition = prev.is_active
        serializer.save()

        current_profile_condition = prev.is_active

        if prev_profile_condition != current_profile_condition:
            if current_profile_condition == True:
                userr = User.objects.get(id=prev.user.id)
                userr.is_active = True
                userr.save()

            else:
                userr = User.objects.get(id=prev.user.id)
                userr.is_active = False
                userr.save()























# {
#     "student":
#     [
#         {
#             "id": 16,
#             "first_name": "sheryf"
#         },
#         {
#             "id": 17,
#             "first_name": "kendrick"
#         }
#     ]
# }


#user
# {
#     "username": "user",
#     "password": "1234"
# }






# TODO super adminpassword

#// TODO report entry for just students in classes
#promote student before you upadt the school


