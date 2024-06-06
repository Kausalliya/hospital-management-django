from django.contrib import admin


from hospital.models import Appointment, Doctor,Patient, PatientDischargeDetails, Treatment


@admin.register(Doctor)
class doctordetailsAdmin(admin.ModelAdmin):
    list_display=('id','doctor','address','gender','mobile','specialization','profile_pic','status')

@admin.register(Patient)
class patientdetailsAdmin(admin.ModelAdmin):
    list_display=('id','patient','address' ,'gender','matrial_status','dob','age','mobile','assignedDoctorId','admitDate','symptoms','status','checkout')

@admin.register(Appointment)
class appointmentdetailsAdmin(admin.ModelAdmin):  
    list_display=('id','patientId','doctorId','patientName','doctorName','appointmentDate','description','mobile','status')  

@admin.register(PatientDischargeDetails)
class PatientDischargeDetailsAdmin(admin.ModelAdmin):  
    list_display= ('id','patientId','doctorId','patientName','doctorName','address','mobile','disease','admitDate','releaseDate','daySpent','roomCharge','medicineCost','doctorFee','OtherCharge','total')

@admin.register(Treatment)
class TreatmentDetailsAdmin(admin.ModelAdmin):  
    list_display=('id','patientid','doctorid','patientname','doctorname','disease','prescribed_medicines')


