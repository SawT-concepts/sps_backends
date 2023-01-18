from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter
from rest_framework_swagger.views import get_swagger_view







# todo would later rename the url nameing here
router = DefaultRouter()
router.register ('get_class', grade_view, basename = "Classes")
router.register('get_students', view_student, basename="Students")
router.register ('school', school_view, basename="School")
router.register('profiles', profile_view, basename= "Profiles")
# router.register('school/<str:pk>', school_view)

schema_view = get_swagger_view(title="SPS doccumentation")


urlpatterns = [
    path('docs/', schema_view),
    path('login', LoginView.as_view(), name="Login"),
    path('tutorials', Tutorial_listapiview.as_view(), name="Tutorial_list"),
    path('get_user_profile_info', get_user_profile.as_view(),
         name="Get User Profile"),
    path('get_school_info', get_short_school_info.as_view(),
         name="Get School Info (short)"),
    path('get_latest_payment', latest_payments.as_view(),
         name="Get Latest Payment"),
    path("report", report_entry_view.as_view(), name="Report Entry"),
    path("bar_graph", bar_graph_view.as_view(), name="Bar Graph"),
    path ("student_payment_graph/<str:grade>", students_graph.as_view(), name="Payment Graph"),
    path('get_student_gd/<str:grade>/',
         get_student_bcAPI.as_view(), name="Student Short"),
    path('get_payment_history/<str:student>', payment_history.as_view(), name= "Payment history"),
    path ('promote_students', Promote_students.as_view(), name="Promote Students"),
    path ("remind-students", Remind_students.as_view(), name= "Remind Students" ),


]

urlpatterns += router.urls




