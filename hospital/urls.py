
from django.urls import path
from hospital import views
from django.contrib.auth.views import LoginView,LogoutView

urlpatterns = [
    path('',views.open_main,name='open_main'),
    path('open_base',views.open_base,name='open_base'),
    path('admin_click',views.admin_click,name='admin_click'),
    path('doc_click',views.doc_click,name='doc_click'),
    path('patient_click',views.patient_click,name='patient_click'),
    path('p_register',views.p_register,name='p_register'),
    path('login',views.login,name='login'),
    path('a_login',views.a_login,name='a_login'),
    path('d_login',views.d_login,name='d_login'),
    path('a_login_to',views.a_login_to,name='a_login_to'),
    path('p_login_to',views.p_login_to,name='p_login_to'),
    path('d_login_to',views.d_login_to,name='d_login_to'),
    path('logout',views.logout,name='logout'),
    path('doctor_register',views.doctor_register,name='doctor_register'),
    path('admin_register',views.admin_register,name='admin_register'),

    #patient
    path('patient_signup',views.patient_signup,name='patient_signup'),
    path('patient_base',views.patient_base,name='patient_base'),
    path('patient_base',views.patient_base,name='patient_base'),
    path('patient_wait',views.patient_wait,name='patient_wait'),
    path('patient_dashboard',views.patient_dashboard,name='patient_dashboard'),
    path('patient_appointment',views.patient_appointment,name='patient_appointment'),
    path('patient_view_appointment/<int:pk>',views.patient_view_appointment,name='patient_view_appointment'),
    path('patient_book_appointment',views.patient_book_appointment,name='patient_book_appointment'),
    path('patient_appointment_submit/<int:pk>',views.patient_appointment_submit,name='patient_appointment_submit'),
    path('patient_view_doctor',views.patient_view_doctor,name='patient_view_doctor'),
    path('search_doctor_view',views.search_doctor_view,name='search_doctor_view'),
    path('patient_discharge',views.patient_discharge,name='patient_discharge'),
    

#doctor
    path('doctor_signup',views.doctor_signup,name='doctor_signup'),
    path('doctor_wait',views.doctor_wait,name='doctor_wait'),
    path('doctor_base',views.doctor_base,name='doctor_base'),
    path('doctor_card',views.doctor_card,name='doctor_card'),
    path('doctor_dashboard',views.doctor_dashboard,name='doctor_dashboard'),
    path('doctor_patient',views.doctor_patient,name='doctor_patient'),
    path('doctor_appointment',views.doctor_appointment,name='doctor_appointment'),
    path('doctor_view_appointment',views.doctor_view_appointment,name='doctor_view_appointment'),
    path('add_treatment_details/<int:pk>',views.add_treatment_details,name='add_treatment_details'),
    path('add_treatment/<int:pk>',views.add_treatment,name='add_treatment'),
    path('doctor_view_patient',views.doctor_view_patient,name='doctor_view_patient'),
    path('doctor_delete_appointment',views.doctor_delete_appointment,name='doctor_delete_appointment'),
    path('d_delete_appointment/<int:pk>',views.d_delete_appointment,name='d_delete_appointment'),
    path('doctor_view_discharge_patient/<int:pk>',views.doctor_view_discharge_patient,name='doctor_view_discharge_patient'),


#admin_doctors
    
    path('admin_signup',views.admin_signup,name='admin_signup'),
    path('admin_base',views.admin_base,name='admin_base'),
    path('admin_card',views.admin_card,name='admin_card'),
    path('admin_dashboard',views.admin_dashboard,name='admin_dashboard'),
    path('admin_doctor',views.admin_doctor,name='admin_doctor'),
    path('admin_doctor_signup',views.admin_doctor_signup,name='admin_doctor_signup'),
    path('admin_view_doctor',views.admin_view_doctor,name='admin_view_doctor'),
    path('admin_add_doctor',views.admin_add_doctor,name='admin_add_doctor'),
    path('doctor_present/<int:pk>',views.doctor_present,name='doctor_present'),
    path('doctor_not_present/<int:pk>',views.doctor_not_present,name='doctor_not_present'),
    path('admin_update_doctor/<int:mk>',views.admin_update_doctor,name='admin_update_doctor'),
    path('update_doctor/<int:mk>',views.update_doctor,name='update_doctor'),
    path('admin_delete_doctor/<int:pk>',views.admin_delete_doctor,name='admin_delete_doctor'),
    path('admin_approve_doctor',views.admin_approve_doctor,name='admin_approve_doctor'),
    path('approve_doctor/<int:pk>',views.approve_doctor,name='approve_doctor'),
    path('approve_delete_doctor/<int:pk>',views.approve_delete_doctor,name='approve_delete_doctor'),
    path('admin_doctor_special',views.admin_doctor_special,name='admin_doctor_special'),
#admin_patient

    path('admin_patient',views.admin_patient,name='admin_patient'),
    path('admin_view_patient',views.admin_view_patient,name='admin_view_patient'),
    path('admin_upadte_patient/<int:pk>',views.admin_update_patient,name='admin_update_patient'),
    path('upadte_patient/<int:pk>',views.update_patient,name='update_patient'),
    path('admin_delete_patient/<int:pk>',views.admin_delete_patient,name='admin_delete_patient'),
    path('admin_add_patient',views.admin_add_patient,name='admin_add_patient'),
    path('admin_patient_signup',views.admin_patient_signup,name='admin_patient_signup'),
    path('admin_approve_patient',views.admin_approve_patient,name='admin_approve_patient'),
    path('approve_patient/<int:pk>',views.approve_patient,name='approve_patient'),
    path('approve_delete_patient/<int:pk>',views.approve_delete_patient,name='approve_delete_patient'),
    path('admin_discharge_patient',views.admin_discharge_patient,name='admin_discharge_patient'),
    path('generate_bill/<int:pk>,<int:mk>',views.generate_bill,name='generate_bill'),
    path('download_pdf/<int:pk>', views.download_pdf,name='download_pdf'),
    path('admin_appointment',views.admin_appointment,name='admin_appointment'),
    path('admin_add_appointment',views.admin_add_appointment,name='admin_add_appointment'),
    path('admin_appointment_submit',views.admin_appointment_submit,name='admin_appointment_submit'),
    path('admin_view_appointment',views.admin_view_appointment,name='admin_view_appointment'),
    path('admin_approve_appointment',views.admin_approve_appointment,name='admin_approve_appointment'),
    path('approve_appointment/<int:pk>',views.approve_appointment,name='approve_appointment'),
    path('delete_appointment/<int:pk>',views.delete_appointment,name='delete_appointment')





]