from django.urls import path
from .views import *
from doctors.views import  doctor_blogs,search_blogs, profile,blogs_category, view_blog, post_comment 
urlpatterns = [
  path('patient_dashboard/', patient_dashboard, name='patient_dashboard'),
  path('profile/', profile, name='patient_profile'),
  
  path('blogs/', doctor_blogs, name='patient_blogs'),
  path('search/',search_blogs,name='search_blogs'),
  path('category/<str:cat>/',blogs_category,name='categories'),
  path('blog/<int:blog_id>/',view_blog,name='blog'),
  path('comment/',post_comment,name='comment'),
  
  path('book_appointment/', book_appointment, name='book_appointment'),
  path('prescription/view/<int:appointment_id>/', view_prescription, name='view_prescription'),
  path('my_appointments/', my_appointments, name='my_appointments'),
  path('patient_confirm_book/<str:doctor>/', patient_confirm_book, name='patient_confirm_book'),
  path('choose-time/<int:appointment_id>/', choose_consultation_time, name='choose_consultation_time'),
  path('payment/<int:appointment_id>/', payment_view, name='payment_view'),
  path('payment-success/<int:appointment_id>/', payment_success, name='payment_success'),

  path('patient-report/', patient_appointment_report, name='report'),

  
]