from email.policy import default
from django.db import models
from django.contrib.auth.models import User

class Doctor(models.Model):
    doctor=models.ForeignKey(User,on_delete=models.CASCADE)
    address = models.CharField(max_length=40,null=True)
    gender=models.CharField(max_length=50,null=True)
    mobile = models.CharField(max_length=20,null=True)
    specialization= models.CharField(max_length=50,default='Emergency Medicine Specialists')
    profile_pic= models.ImageField(upload_to='profile_pic/',null=True,blank=True)
    status=models.BooleanField(default=False)
    absent=models.BooleanField(default=False)
    @property
    def get_name(self):
        return self.doctor.first_name+" "+self.doctor.last_name
class Patient(models.Model):
    patient=models.ForeignKey(User,on_delete=models.CASCADE)
    address = models.CharField(max_length=40,null=True)
    gender=models.CharField(max_length=50,null=True)
    matrial_status=models.CharField(max_length=50,null=True)
    dob=models.DateField(max_length=8,null=True, blank=True)
    age=models.IntegerField(null=True, blank=True)
    mobile = models.CharField(max_length=20,null=True)
    assignedDoctorId = models.PositiveIntegerField(null=True)
    admitDate=models.DateField(auto_now=True)
    symptoms = models.CharField(max_length=100,null=True)
    status=models.BooleanField(default=False)
    checkout=models.BooleanField(default=False)
    @property
    def get_name(self):
        return self.patient.first_name+" "+self.patient.last_name
    
class Appointment(models.Model):
    patientId=models.PositiveIntegerField(null=True)
    doctorId=models.PositiveIntegerField(null=True)
    patientName=models.CharField(max_length=40,null=True)
    doctorName=models.CharField(max_length=40,null=True)
    appointmentDate=models.DateField(auto_now=True)
    description=models.TextField(max_length=500)
    mobile=models.CharField(max_length=15,null=True)
    status=models.BooleanField(default=False)



class PatientDischargeDetails(models.Model):
    patientId=models.PositiveIntegerField(null=True)
    doctorId=models.PositiveIntegerField(null=True)
    patientName=models.CharField(max_length=40)
    doctorName=models.CharField(max_length=40,null=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=True)
    disease= models.CharField(max_length=100,null=True)
    admitDate=models.DateField(null=False)
    releaseDate=models.DateField(null=False)
    daySpent=models.PositiveIntegerField(null=False)

    roomCharge=models.PositiveIntegerField(null=False)
    medicineCost=models.PositiveIntegerField(null=False)
    doctorFee=models.PositiveIntegerField(null=False)
    OtherCharge=models.PositiveIntegerField(null=False)
    total=models.PositiveIntegerField(null=False)

class Treatment(models.Model):
    patientid=models.PositiveIntegerField(null=True)
    doctorid=models.PositiveIntegerField(null=True)
    patientname=models.CharField(max_length=40,null=True)
    doctorname=models.CharField(max_length=40,null=True)
    disease=models.CharField(max_length=90,null=True)
    prescribed_medicines=models.CharField(max_length=500,null=True)


