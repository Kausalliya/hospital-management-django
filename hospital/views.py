
from __future__ import unicode_literals
from django.shortcuts import render,redirect,reverse
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required,user_passes_test
from datetime import datetime,timedelta,date
from django.db.models import Q
import random
from django.conf import settings


import io
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from django.contrib.sessions.models import Session
Session.objects.all().delete()

from hospital.models import Appointment, Patient,Doctor, PatientDischargeDetails, Treatment

def open_main(request):
    return render(request,'main.html')

def open_base(request):
    return render(request,'base.html')
   
def admin_click(request):
    return render(request,'admin_click.html')    

def doc_click(request):
    return render(request,'doc_click.html')    

def patient_click(request):
    return render(request,'patient_click.html')    

def p_register(request):
    numbers = '1234567890'
    small_letters = "qwertyuioplkjhgfdsazxcvbnm"
    upper_case = "QWERTYUIOPASDFGHJKLMNBVCXZ"
    prep =numbers + small_letters + upper_case
    thepassword = ''.join(random.sample(prep,8))
    print(thepassword)
    return render(request,'patient_register.html',{'pass':thepassword})    

def admin_register(request):
    return render(request,'admin_register.html') 

def logout(request):
	auth.logout(request)
	return redirect('open_main') 

def login(request):
    return render(request,'p_login.html')

def a_login(request):
    return render(request,'a_login.html')   

def d_login(request):
    return render(request,'d_login.html')   

def doctor_register(request):
    numbers = '1234567890'
    small_letters = "qwertyuioplkjhgfdsazxcvbnm"
    upper_case = "QWERTYUIOPASDFGHJKLMNBVCXZ"
    prep =numbers + small_letters + upper_case
    thepassword = ''.join(random.sample(prep,8))
    print(thepassword)
    return render(request,'doctor_register.html',{'pass':thepassword}) 

def doctor_wait(request) :
    return render(request,'doctor_wait.html') 

def patient_wait(request) :
    return render(request,'patient_wait.html')   

def a_login_to(request):
    if request.method=='POST':
        username=request.POST['uname']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            if is_admin(user):
                auth.login(request,user)
                return redirect('admin_dashboard')
            else:
                messages.info(request, 'Invalid Username or Password. Try Again.')
                return redirect('a_login')     
        else:
            messages.info(request, 'Invalid Username or Password. Try Again.')
            return redirect('a_login') 
    else:
        return redirect('open_main')

def d_login_to(request):
    if request.method=='POST':
        username=request.POST['uname']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            if is_doctor(user):
                accountapproval=Doctor.objects.all().filter(doctor_id=user.id,status=True)
                if accountapproval:
                   auth.login(request,user)
                   return redirect('doctor_dashboard')
                else:
                   return render(request,'doctor_wait.html',{'user':user})
            else:
                messages.info(request, 'Invalid Username or Password. Try Again.')
                return redirect('d_login')       
        else:
            messages.info(request, 'Invalid Username or Password. Try Again.')
            return redirect('d_login') 
    else:
        return redirect('open_main')  

def p_login_to(request):
    if request.method=='POST':
        username=request.POST['uname']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None:              
            if is_patient(user):
                accountapproval=Patient.objects.all().filter(patient_id=user.id,status=True)
                if accountapproval:
                    auth.login(request,user)
                    return redirect('patient_dashboard')
                else:
                    return render(request,'patient_wait.html',{'user':user}) 
            else:
                messages.info(request, 'Invalid Username or Password. Try Again.')
                return redirect('login')        
        else:
            messages.info(request, 'Invalid Username or Password. Try Again.')
            return redirect('login') 
    else:
        return redirect('open_main')              
              
                    

def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()
def is_doctor(user):
    return user.groups.filter(name='DOCTOR').exists()
def is_patient(user):
    return user.groups.filter(name='PATIENT').exists()
 



#---patient views
def patient_signup(request):
   if request.method=='POST':
        first_name=request.POST['fname']
        last_name=request.POST['lname']
        address=request.POST['address']
        gender=request.POST['gender']
        dob=request.POST['dob']
        msta=request.POST['mstatus']
        age=request.POST['age']
        num=request.POST['number']
        username=request.POST['uname']
        email=request.POST['email']
        password=request.POST['password']
        cpassword=request.POST['cpassword']
        if password==cpassword: 
            if User.objects.filter(username=username).exists(): 
                messages.info(request, 'This username already exists!!!!')
                return redirect('p_register')
            else:
                user=User.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    email=email,
                    password=password,
                    )
                user.save()
                patient=User.objects.get(username=username)
                data =Patient(patient=patient,address=address,gender=gender,matrial_status=msta,dob=dob,age=age,mobile=num)  
                data.save()
                my_patient_group = Group.objects.get_or_create(name='PATIENT')
                my_patient_group[0].user_set.add(user)
                messages.success(request, "Registered successfully")
        else:
            messages.info(request, 'Password doesnt match!!!!!!!')
            print("Password is not Matching.. ") 
            return redirect('p_register')   
        return redirect('p_register')           

@login_required(login_url='p_login_to')
def patient_base(request):
    return render(request,'patient_base.html') 

@login_required(login_url='p_login_to')
def patient_card(request): 
    patient=Patient.objects.get(patient_id=request.user.id)
    if patient.assignedDoctorId is None:
        data="Not Appointed"
        no="No Diagnosis "
    else:
        doctor=Doctor.objects.get(id=patient.assignedDoctorId)
        return render(request,'patient_dashboard.html',{'doctor':doctor,'patient':patient}) 
    return render(request,'patient_dashboard_cards.html',{'data':data,'no':no}) 


def patient_dashboard(request):
    patient=Patient.objects.get(patient_id=request.user.id)
    if patient.assignedDoctorId is None:
        data="Not Appointed"
        no="No Diagnosis "
    else:
        doctor=Doctor.objects.get(id=patient.assignedDoctorId)
        return render(request,'patient_dashboard.html',{'doctor':doctor,'patient':patient})     
    return render(request,'patient_dashboard.html',{'data':data,'no':no})    

@login_required(login_url='p_login_to')
def patient_appointment(request):
    return render(request,'patient_appointment.html')

@login_required(login_url='p_login_to')
def patient_view_appointment(request,pk):
    patient=Patient.objects.get(patient_id=pk)
    app=Appointment.objects.all().filter(patientId=patient.id)
    return render(request,'patient_view_appointment.html.',{'app':app})    

@login_required(login_url='p_login_to')
def patient_book_appointment(request):
    doctors=Doctor.objects.all().filter(status=True,absent=True) 
    return render(request,'patient_book_appointment.html',{'doc':doctors})

@login_required(login_url='p_login_to')
def patient_appointment_submit(request,pk):
    patient=Patient.objects.get(patient_id=pk)
    if request.method=='POST':
        dname=request.POST['dname']
        pname=request.POST['pname']
        des=request.POST['des']
        doctor=Doctor.objects.get(id=dname)
        duser=User.objects.get(id=doctor.doctor_id)
        data=Appointment(patientId=patient.id,doctorId=dname,description=des,doctorName=duser.first_name,patientName=pname,mobile=patient.mobile)
        data.save()
    return redirect('patient_view_appointment',pk)    

@login_required(login_url='p_login_to')
def patient_view_doctor(request):
    doctors=Doctor.objects.all().filter(status=True)
    return render(request,'patient_view_doctor.html',{'doctors':doctors})

@login_required(login_url='p_login_to')
def search_doctor_view(request):
    query = request.GET['query']
    doctor=Doctor.objects.all().filter(status=True)
    doctors=Doctor.objects.all().filter(status=True).filter(Q(specialization__icontains=query))
    return render(request,'patient_view_doctor.html',{'doctors':doctors})

@login_required(login_url='p_login_to')
def patient_discharge(request):
    patient=Patient.objects.get(patient_id=request.user.id) 
    dischargeDetails=PatientDischargeDetails.objects.all().filter(patientId=patient.id).order_by('-id')[:1]
    patientDict=None
    if dischargeDetails:
        patientDict ={
        'is_discharged':True,
        'patient':patient,
        'patientId':patient.id,
        'patientName':dischargeDetails[0].patientName,
        'assignedDoctorName':dischargeDetails[0].doctorName,
        'address':patient.address,
        'symptoms':dischargeDetails[0].disease,
        'mobile':patient.mobile,
        'admitDate':patient.admitDate,
        'releaseDate':dischargeDetails[0].releaseDate,
        'daySpent':dischargeDetails[0].daySpent,
        'medicineCost':dischargeDetails[0].medicineCost,
        'roomCharge':dischargeDetails[0].roomCharge,
        'doctorFee':dischargeDetails[0].doctorFee,
        'OtherCharge':dischargeDetails[0].OtherCharge,
        'total':dischargeDetails[0].total,
        }
        print(patientDict)
    else:
        patientDict={
            'is_discharged':False,
            'patient':patient,
            'patientId':request.user.id,
        }
    return render(request,'patient_discharge.html',context=patientDict)





#doctor views
@login_required(login_url='d_login_to')
def doctor_base(request):
    return render(request,'doctor_base.html') 

@login_required(login_url='d_login_to')
def doctor_card(request):
    return render(request,'doctor_dashboard_cards.html') 

@login_required(login_url='d_login_to')
def doctor_dashboard(request):
    doctor=Doctor.objects.get(doctor_id=request.user.id)
    appointments=Appointment.objects.filter(status=True,doctorId=doctor.id).count()
    patients=Patient.objects.all().filter(status=True,assignedDoctorId=doctor.id,checkout=False).count()
    dischargedpatients=PatientDischargeDetails.objects.all().distinct().filter(doctorId=doctor.id).count()
    app=Appointment.objects.filter(status=True,doctorId=doctor.id).order_by('-id')
    return render(request,'doctor_dashboard.html',{'doctor':doctor,'a':appointments,'p':patients,'pd':dischargedpatients,'app':app})
    
@login_required(login_url='d_login_to')
def doctor_patient(request):
    doctor=Doctor.objects.get(doctor_id=request.user.id)
    return render(request,'doctor_patient.html',{'doctor':doctor})

def doctor_signup(request):
    if request.method=='POST':
        first_name=request.POST['fname']
        last_name=request.POST['lname']
        address=request.POST['address']
        gender=request.POST['gender']
        num=request.POST['number']
        select=request.POST['select']
        file=request.FILES['pic']
        username=request.POST['uname']
        email=request.POST['email']
        password=request.POST['password']
        cpassword=request.POST['cpassword']
        if password==cpassword: 
            if User.objects.filter(username=username).exists(): 
                messages.info(request, 'This username already exists!!!!')
                return redirect('doctor_register')
            else:
                user=User.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    email=email,
                    password=password,
                    )
                user.save()
                doctor=User.objects.get(username=username)
                data =Doctor(doctor=doctor,address=address,gender=gender,mobile=num,specialization=select,profile_pic=file)  
                data.save()
                my_doctor_group = Group.objects.get_or_create(name='DOCTOR')
                my_doctor_group[0].user_set.add(user)
                messages.success(request, "Registered successfully")
        else:
            messages.info(request, 'Password doesnt match!')
            print("Password is not Matching.. ") 
            return redirect('doctor_register')   
        return redirect('doctor_register') 


@login_required(login_url='d_login_to')
def doctor_appointment(request):
    doctor=Doctor.objects.get(doctor_id=request.user.id)
    return render(request,'doctor_appointment.html',{'doctor':doctor})


@login_required(login_url='d_login_to')
def doctor_view_appointment(request):
    doctor=Doctor.objects.get(doctor_id=request.user.id)
    appointments=Appointment.objects.filter(status=True,doctorId=doctor.id).order_by('-id')
    return render(request,'doctor_view_appointment.html',{'appointments':appointments,'doctor':doctor}) 


@login_required(login_url='d_login_to')
def doctor_delete_appointment(request):
    doctor=Doctor.objects.get(doctor_id=request.user.id)
    appointments=Appointment.objects.filter(status=True,doctorId=doctor.id).order_by('-id')
    return render(request,'doctor_delete_appointment.html',{'appointments':appointments,'doctor':doctor})       


@login_required(login_url='d_login_to')
def d_delete_appointment(request,pk):
    app=Appointment.objects.get(id=pk)
    app.delete()
    return redirect('doctor_delete_appointment')


@login_required(login_url='d_login_to')
def add_treatment_details(request,pk):
    doctor=Doctor.objects.get(doctor_id=request.user.id)
    patient=Patient.objects.get(id=pk)
    return render(request,'add_treatment_details.html',{'doctor':doctor,'patient':patient})  


@login_required(login_url='d_login_to')
def add_treatment(request,pk):
    doctor=Doctor.objects.get(doctor_id=request.user.id)
    duser=User.objects.get(id=doctor.doctor_id)
    patient=Patient.objects.get(id=pk)
    puser=User.objects.get(id=patient.patient_id)
    if request.method=='POST':
        disease=request.POST['disease']
        medicine=request.POST['medicine']
    treatment=Treatment(patientid=pk,doctorid=doctor.id,patientname=puser.first_name,doctorname=duser.first_name,disease=disease,prescribed_medicines=medicine) 
    patient.assignedDoctorId=doctor.id
    patient.symptoms=disease
    patient.checkout=False
    patient.save()       
    treatment.save()
    return redirect('doctor_view_appointment')

@login_required(login_url='d_login_to')
def doctor_view_patient(request):
    doctor=Doctor.objects.get(doctor_id=request.user.id)
    patients=Patient.objects.all().filter(status=True,assignedDoctorId=doctor.id,checkout=False).order_by('-id')
    return render(request,'doctor_view_patient.html',{'doctor':doctor,'patients':patients}) 


@login_required(login_url='d_login_to')
def doctor_view_discharge_patient(request,pk):
    doctor=Doctor.objects.get(doctor_id=pk) 
    dischargedpatients=PatientDischargeDetails.objects.all().distinct().filter(doctorId=doctor.id)
    return render(request,'doctor_view_discharge_patient.html',{'dischargedpatients':dischargedpatients,'doctor':doctor})    


#admin views



def admin_signup(request):
    if request.method=='POST':
        first_name=request.POST['fname']
        last_name=request.POST['lname']
        email=request.POST['email']
        username=request.POST['uname']
        password=request.POST['password']
        cpassword=request.POST['cpassword']
        if password==cpassword: 
            if User.objects.filter(username=username).exists(): 
                messages.info(request, 'This username already exists!!!!')
                return redirect('admin_register')
            else:
                user=User.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    password=password,
                    email=email
                    )
                user.save()
                User.is_staff=True
                User.save()
                my_admin_group = Group.objects.get_or_create(name='Admin')
                my_admin_group[0].user_set.add(user)
                messages.success(request, "Registered successfully")
        else:
            messages.info(request, 'Password doesnt match!!!!!!!')
            print("Password is not Matching.. ") 
            return redirect('admin_register')   
        return redirect('admin_register') 

@login_required(login_url='a_login_to')
def admin_base(request):
    return render(request,'admin_base.html')               

@login_required(login_url='a_login_to')
def admin_card(request):
    return render(request,'admin_dashboard_cards.html') 

@login_required(login_url='a_login_to')
def admin_dashboard(request):
    doctors=Doctor.objects.all().order_by('-id')
    patients=Patient.objects.all().order_by('-id')
    doctorcount=Doctor.objects.all().filter(status=True).count()
    pendingdoctorcount=Doctor.objects.all().filter(status=False).count()
    patientcount=Patient.objects.all().filter(status=True).count()
    pendingpatientcount=Patient.objects.all().filter(status=False).count()
    appointmentcount=Appointment.objects.all().filter(status=True).count()
    pendingappointmentcount=Appointment.objects.all().filter(status=False).count()
    mydict={
    'doctors':doctors,
    'patients':patients,
    'doctorcount':doctorcount,
    'pendingdoctorcount':pendingdoctorcount,
    'patientcount':patientcount,
    'pendingpatientcount':pendingpatientcount,
    'appointmentcount':appointmentcount,
    'pendingappointmentcount':pendingappointmentcount,
    }
    return render(request,'admin_dashboard.html',context=mydict)   

@login_required(login_url='a_login_to')
def admin_doctor(request):
    return render(request,'admin_doctor.html')

@login_required(login_url='a_login_to')
def admin_add_doctor(request):
    return render(request,'admin_add_doctor.html')

@login_required(login_url='a_login_to')
def doctor_present(request,pk):
    doctors=Doctor.objects.get(id=pk)
    doctors.absent=True
    doctors.save()
    return redirect('admin_view_doctor')

@login_required(login_url='a_login_to')
def doctor_not_present(request,pk):
    doctors=Doctor.objects.get(id=pk)
    doctors.absent=False
    doctors.save()
    return redirect('admin_view_doctor')


@login_required(login_url='a_login_to')
def admin_update_doctor(request,mk):
    doctors=Doctor.objects.get(id=mk)
    return render(request,'admin_update_doctor.html',{'d':doctors})    

@login_required(login_url='a_login_to')
def update_doctor(request,mk):
    doctors=Doctor.objects.get(id=mk)
    user=User.objects.get(id=doctors.doctor_id)
    doctors.address=request.POST['address']
    doctors.gender=request.POST['gender']
    doctors.mobile=request.POST['number']
    doctors.specialization=request.POST['select']
    user.first_name=request.POST['fname']
    user.last_name=request.POST['lname']
    user.username=request.POST['uname']
    if request.POST.get('select') is not None:
        doctors.specialization=request.POST.get('select')
    else:
        doctors.specialization=doctors.specialization    
    if request.FILES.get('pic')  is not None:
        doctors.profile_pic=request.FILES.get('pic') 
    else:
        doctors.profile_pic= doctors.profile_pic   
    user.save()
    doctors.save()
    return redirect('admin_view_doctor') 

@login_required(login_url='a_login_to')
def admin_delete_doctor(request,pk):
    doct=Doctor.objects.get(id=pk)
    user=User.objects.get(id=doct.doctor_id)
    doc=Patient.objects.filter(assignedDoctorId=pk)
    doc.assignedDoctorId="Null"
    user.delete()
    doct.delete()
    return redirect('admin_view_doctor')           

@login_required(login_url='a_login_to')
def admin_approve_doctor(request):
    doctors=Doctor.objects.all().filter(status=False)
    return render(request,'admin_approve_doctor.html',{'doctors':doctors}) 

@login_required(login_url='a_login_to')
def approve_doctor(request,pk):
    doctor=Doctor.objects.get(id=pk)
    doctor.status=True
    doctor.save()
    return redirect('admin_approve_doctor')    

@login_required(login_url='a_login_to')
def approve_delete_doctor(request,pk):
    doctor=Doctor.objects.get(id=pk)
    user=User.objects.get(id=doctor.doctor_id)
    user.delete()
    doctor.delete()
    return redirect('admin_approve_doctor')       


@login_required(login_url='a_login_to')
def admin_view_doctor(request):
    doctors=Doctor.objects.all().filter(status=True)
    return render(request,'admin_view_doctor.html',{'doctors':doctors})

@login_required(login_url='a_login_to')
def admin_doctor_special(request):
    doctors=Doctor.objects.all().filter(status=True)
    return render(request,'admin_view_doctor_Specialisation.html',{'doctors':doctors})    

@login_required(login_url='a_login_to')
def admin_doctor_signup(request):
    if request.method=='POST':
        first_name=request.POST['fname']
        last_name=request.POST['lname']
        address=request.POST['address']
        gender=request.POST['gender']
        num=request.POST['number']
        select=request.POST['select']
        file=request.FILES['pic']
        username=request.POST['uname']
        email=request.POST['email']
        characters=list('0123456789')
        characters.extend(list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))
        characters.extend(list('0123456789'))
        characters.extend(list('!@#$%^&*()?><:;'))
        thepassword = ''
        for x in range(8):
            thepassword += random.choice(characters)
        print(thepassword)
        if User.objects.filter(username=username).exists(): 
                messages.info(request, 'This username already exists!!!!')
                return redirect('admin_add_doctor')
        else:
                user=User.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    email=email,
                    password=thepassword,
                    )
                user.save()
                doctor=User.objects.get(username=username)
                data =Doctor(doctor=doctor,address=address,gender=gender,mobile=num,specialization=select,profile_pic=file)  
                data.save()
                my_doctor_group = Group.objects.get_or_create(name='DOCTOR')
                my_doctor_group[0].user_set.add(user)
                subject='Sri MHS Hospital-Your User and Password'
                content="username:"+username+"password:"+thepassword
                send_mail(subject,content,settings.EMAIL_HOST_USER,[email])
        return redirect('admin_approve_doctor') 


@login_required(login_url='a_login_to')
def admin_patient(request):
    return render(request,'admin_patient.html') 

@login_required(login_url='a_login_to')
def admin_view_patient(request):
    patient=Patient.objects.all().filter(status=True).order_by('-id')  
    return render(request,'admin_view_patient.html',{'patients':patient})   

@login_required(login_url='a_login_to')   
def admin_update_patient(request,pk):
    patient=Patient.objects.get(id=pk)  
    return render(request,'admin_update_patient.html',{'p':patient})       

@login_required(login_url='a_login_to')
def update_patient(request,pk):
    patient=Patient.objects.get(id=pk) 
    user=User.objects.get(id=patient.patient_id)
    patient.address=request.POST['address']
    patient.gender=request.POST['gender']
    patient.mobile=request.POST['number']
    patient.age=request.POST['age']
    patient.matrial_status=request.POST['mstatus']
    patient.do
    b=request.POST['dob']
    user.first_name=request.POST['fname']
    user.last_name=request.POST['lname']
    user.username=request.POST['uname']
    patient.save()
    user.save()
    return redirect('admin_view_patient')          

@login_required(login_url='a_login_to')
def admin_delete_patient(request,pk):
    p=Patient.objects.get(id=pk)
    user=User.objects.get(id=p.patient_id)
    user.delete()
    p.delete()
    return redirect('admin_view_patient') 

@login_required(login_url='a_login_to')
def admin_add_patient(request):
    return render(request,'admin_add_patient.html')    

@login_required(login_url='a_login_to') 
def admin_patient_signup(request):
    if request.method=='POST':
        first_name=request.POST['fname']
        last_name=request.POST['lname']
        address=request.POST['address']
        gender=request.POST['gender']
        dob=request.POST['dob']
        msta=request.POST['mstatus']
        age=request.POST['age']
        num=request.POST['number']
        username=request.POST['uname']
        email=request.POST['email'] 
        characters=list('0123456789')
        characters.extend(list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))
        characters.extend(list('0123456789'))
        characters.extend(list('!@#$%^&*()?><:;'))
        thepassword = ''
        for x in range(8):
            thepassword += random.choice(characters)
        print(thepassword)
        if User.objects.filter(username=username).exists(): 
                messages.info(request, 'This username already exists!!!!')
                return redirect('admin_add_patient')
        else:
                user=User.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    email=email,
                    password=thepassword,
                    )
                user.save()
                patient=User.objects.get(username=username)
                data =Patient(patient=patient,address=address,gender=gender,matrial_status=msta,dob=dob,age=age,mobile=num)  
                data.save()
                my_patient_group = Group.objects.get_or_create(name='PATIENT')
                my_patient_group[0].user_set.add(user)
                subject='Sri MHS Hospital-Your User and Password'
                content="username:"+username+"password:"+thepassword
                send_mail(subject,content,settings.EMAIL_HOST_USER,[email])  
        return redirect('admin_approve_patient')

@login_required(login_url='a_login_to')
def admin_approve_patient(request):
    patients=Patient.objects.all().filter(status=False).order_by('-id')
    return render(request,'admin_approve_patient.html',{'patients':patients})

@login_required(login_url='a_login_to')
def approve_patient(request,pk):
    patient=Patient.objects.get(id=pk)
    patient.status=True
    patient.save()
    return redirect('admin_approve_patient')

@login_required(login_url='a_login_to')
def approve_delete_patient(request,pk):
    patient=Patient.objects.get(id=pk)
    user=User.objects.get(id=patient.patient_id)
    user.delete()
    patient.delete()
    return redirect('admin_approve_patient')  

@login_required(login_url='a_login_to')
def admin_discharge_patient(request):
    patients=Patient.objects.all().filter(status=True,assignedDoctorId__isnull = False,checkout=False).order_by('-id')
    return render(request,'admin_discharge_patient.html',{'patients':patients}) 

@login_required(login_url='a_login_to')
def generate_bill(request,pk,mk):
    patient=Patient.objects.get(id=pk)
    user=User.objects.get(id=patient.patient_id)
    days=(date.today()-patient.admitDate)
    assignedDoctor=Doctor.objects.get(id=mk)
    duser=User.objects.get(id=assignedDoctor.doctor_id)
    d=days.days 
    patientDict={
        'patientId':pk,
        'fname':user.first_name,
        'lname':user.last_name,
        'mobile':patient.mobile,
        'address':patient.address,
        'symptoms':patient.symptoms,
        'admitDate':patient.admitDate,
        'todayDate':date.today(),
        'day':d,
        'assignedDoctorName':duser.first_name,
        'assignedDoctorlName':duser.last_name
    }
    if request.method == 'POST':
        feeDict ={
            'roomCharge':int(request.POST['roomCharge'])*int(d),
            'doctorFee':request.POST['doctorFee'],
            'medicineCost' : request.POST['medicineCost'],
            'OtherCharge' : request.POST['OtherCharge'],
            'total':(int(request.POST['roomCharge'])*int(d))+int(request.POST['doctorFee'])+int(request.POST['medicineCost'])+int(request.POST['OtherCharge'])
        }
        patientDict.update(feeDict)
        pDD=PatientDischargeDetails()
        pDD.patientId=pk
        pDD.doctorId=mk
        pDD.patientName=user.first_name
        pDD.doctorName=duser.first_name
        pDD.address=patient.address
        pDD.mobile=patient.mobile
        pDD.disease=patient.symptoms
        pDD.admitDate=patient.admitDate
        pDD.releaseDate=date.today()
        pDD.daySpent=int(d)
        pDD.discharged=True
        pDD.medicineCost=int(request.POST['medicineCost'])
        pDD.roomCharge=int(request.POST['roomCharge'])*int(d)
        pDD.doctorFee=int(request.POST['doctorFee'])
        pDD.OtherCharge=int(request.POST['OtherCharge'])
        pDD.total=(int(request.POST['roomCharge'])*int(d))+int(request.POST['doctorFee'])+int(request.POST['medicineCost'])+int(request.POST['OtherCharge'])
        pDD.save()
        patient.checkout=True
        patient.save()
        return render(request,'patient_final_bill.html',context=patientDict)
    return render(request,'patient_generate_bill.html',context=patientDict)


def download_pdf(request,pk):
    dischargeDetails=PatientDischargeDetails.objects.all().filter(patientId=pk).order_by('-id')[:1]
    dict={
        'patientName':dischargeDetails[0].patientName,
        'assignedDoctorName':dischargeDetails[0].doctorName,
        'address':dischargeDetails[0].address,
        'mobile':dischargeDetails[0].mobile,
        'symptoms':dischargeDetails[0].disease,
        'admitDate':dischargeDetails[0].admitDate,
        'releaseDate':dischargeDetails[0].releaseDate,
        'daySpent':dischargeDetails[0].daySpent,
        'medicineCost':dischargeDetails[0].medicineCost,
        'roomCharge':dischargeDetails[0].roomCharge,
        'doctorFee':dischargeDetails[0].doctorFee,
        'OtherCharge':dischargeDetails[0].OtherCharge,
        'total':dischargeDetails[0].total,
    }
    return render_to_pdf('download_bill.html',dict)


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return    

@login_required(login_url='a_login_to')     
def admin_appointment(request):
    return render(request,'admin_appointment.html')

@login_required(login_url='a_login_to')
def admin_add_appointment(request):
    doctors=Doctor.objects.all().filter(status=True,absent=True)
    patient=Patient.objects.all().filter(status=True).order_by('-id')
    return render(request,'admin_add_appointment.html',{'doc':doctors,'patient':patient}) 

@login_required(login_url='a_login_to')
def admin_appointment_submit(request):
    if request.method=='POST':
        dname=request.POST['dname']
        pname=request.POST['pname']
        des=request.POST['des']
        patient=Patient.objects.get(id=pname)
        puser=User.objects.get(id=patient.patient_id)
        doctor=Doctor.objects.get(id=dname)
        duser=User.objects.get(id=doctor.doctor_id)
        data=Appointment(patientId=pname,doctorId=dname,description=des,status=True,doctorName=duser.first_name,patientName=puser.first_name,mobile=patient.mobile)
        data.save()
        return redirect('admin_view_appointment')

@login_required(login_url='a_login_to')
def admin_view_appointment(request):
    appointments=Appointment.objects.all().filter(status=True).order_by('-id')
    return render(request,'admin_view_appointment.html',{'appointments':appointments})

@login_required(login_url='a_login_to')
def admin_approve_appointment(request):
    appointments=Appointment.objects.all().filter(status=False)
    return render(request,'admin_approve_appointment.html',{'appointments':appointments})    

@login_required(login_url='a_login_to')
def approve_appointment(request,pk):
    app=Appointment.objects.get(id=pk)
    app.status=True
    app.save()
    return redirect('admin_approve_appointment')

@login_required(login_url='a_login_to')
def delete_appointment(request,pk):
    app=Appointment.objects.get(id=pk)
    app.delete()
    return redirect('admin_approve_appointment',)
