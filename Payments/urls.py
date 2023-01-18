from django.urls import path
from .views import *

urlpatterns = [
    path('<str:school_id>', home_payment, name= "home_payment"),
    path ('settled/<str:student_id>', no_pay, name="no_pay"),
    path ('input-amount/<str:payment_id>', input_amount, name="input amount"),
    path('initiate-payment/<str:payment_id>', initiate_payment, name="initiate_payment"),
    path('verify-payment/<str:ref>', verify_payment, name="verify_payment"),
    path('success/<str:payment_id>', success_payment, name="success"),
    path ('reciept/<str:payment_id>', render_pdf_view, name= "Generate pdf"),
    path('verify-reciept/<str:payment_id>', verify_reciept, name="verify_reciept"),
]
