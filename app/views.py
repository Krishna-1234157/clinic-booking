from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.contrib import messages

# Create your views here.

def index(request):
    return render(request, 'index.html')

def patient_register(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        notes = request.POST['notes']
        username = request.POST['username']
        password = request.POST['password']
        data1 = Patient.objects.create(name=name, email=email, phone=phone, notes=notes, username=username, password=password)
        data1.save()
        data2 = Login.objects.create(username=username, password=password)
        data2.save()
        messages.success(request, "Patient registered")
        return render(request, 'login.html')
    else:
        return render(request, 'register.html')



def profile(request):
    if 'id' in request.session:  #session check
        user = request.session['id']
        data = Patient.objects.filter(username=user)
        return render(request, 'user.html', {'data':data})
    else:
        doctor = Doctor.objects.all()
        return render(request,'index.html',{'data':doctor})


def log(request):
    if request.method == 'POST':
        u = request.POST['username']
        p = request.POST['password']
        if u == 'admin' and p == 'admin':
            return redirect(admin_dashboard)
        else:
            try:
                d = Login.objects.get(username=u)
                if d.password == p:
                    request.session['id'] = u  #session created
                    return redirect(user_page)
                else:
                    messages.error(request, "Password incorrect")
            except Login.DoesNotExist:
                messages.error(request, "Username incorrect")
    else:
        return render(request, 'login.html')


def Logout(request):
    request.session.flush()
    return redirect(profile)



def admin_dashboard(request):
    d = Doctor.objects.all()
    appointment = Appointment.objects.all()
    total_doctors = Doctor.objects.count()
    total_patients = Patient.objects.count()
    total_appointments = Appointment.objects.count()

    return render(request, 'admin.html', {
        'all' : d,
        'appointment' : appointment,
        'doctors': total_doctors,
        'patients': total_patients,
        'appointments': total_appointments
    })

def add_doctor(request):
    if request.method == 'POST':
        name = request.POST['name']
        s = request.POST['specialization']
        day = request.POST['days']
        start_time = request.POST['start_time']
        end_time = request.POST['end_time']
        data = Doctor.objects.create(name=name, specialization=s, available_days=day, start_time=start_time, end_time=end_time)
        data.save()
        messages.success(request, "Doctor Added")
        return redirect(admin_dashboard)
    else:
        return render(request, 'doctor.html')



def user_page(request):
    d = Doctor.objects.all()
    total_doctors = Doctor.objects.count()
    total_patients = Patient.objects.count()
    total_appointments = Appointment.objects.count()

    return render(request, 'user.html', {
        'all': d,
        'doctors': total_doctors,
        'patients': total_patients,
        'appointments': total_appointments
    })


def book_appointment(request):
    doctors = Doctor.objects.all()
    username = request.session.get('id')
    try:
        patient = Patient.objects.get(username=username)
    except Patient.DoesNotExist:
        messages.error(request, "Patient not found")
        return redirect(log)
    if request.method == "POST":
        doctor_id = request.POST['doctor']
        day = request.POST['day']
        slot = request.POST['slot']
        doctor = Doctor.objects.get(id=doctor_id)
        if Appointment.objects.filter(doctor=doctor, day=day, time_slot=slot).exists():
            messages.error(request,"Slot already booked")
        else:
            Appointment.objects.create(
                patient=patient,
                doctor=doctor,
                day=day,
                time_slot=slot
            )
            messages.success(request,"Appointment booked")

    return render(request,"appointment.html",{"doctors":doctors})



def user_dashboard(request):
    username = request.session['id']  # correct session key
    user = Patient.objects.get(username=username)
    appointments = Appointment.objects.filter(patient=user)
    return render(request, 'profile.html', {
        'patient': user,
        'appointments': appointments
    })


def cancel_appointment(request, appointment_id):
    if 'id' in request.session:
        appointment = Appointment.objects.get(id=appointment_id)
        if appointment.patient.username == request.session['id']:
            appointment.delete()
            messages.success(request, "Appointment cancelled successfully.")
        else:
            messages.error(request, "You are not allowed to cancel this appointment.")
        return redirect(profile)
    else:
        messages.error(request, "Please login first.")
        return redirect(log)