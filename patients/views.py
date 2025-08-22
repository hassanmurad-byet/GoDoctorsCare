from gettext import translation
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.core.paginator import Paginator
from django.urls import reverse
from users.models import Doctors , Specialty , Patients
from patients.models import Appointment, Consultation , Time 
import datetime as dt  # for time parsing
from django.db.models import Q
from django.http import HttpResponse, Http404
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

User = get_user_model()


@login_required(login_url='/login')
def patient_dashboard(request):
  return render(request,'patients/patient_dashboard.html')




# @login_required(login_url='/login')
# def my_appointments(request):
#     appointments = Appointment.objects.filter(patient__user=request.user).order_by('-start_date')

#     filter_status = request.GET.get('filter_status')
#     filter_date = request.GET.get('filter_date')
#     filter_doctor_name = request.GET.get('filter_doctor_name')

#     if filter_status and filter_status != 'All':
#         appointments = appointments.filter(status__status=filter_status)

#     if filter_date:
#         appointments = appointments.filter(start_date__date=filter_date)

#     if filter_doctor_name:
#         appointments = appointments.filter(doctor__user__first_name__icontains=filter_doctor_name)

#     return render(request, "patients/my_appointments.html", {
#         'appointments': appointments,
#         'filter_status': filter_status,
#         'filter_date': filter_date,
#         'filter_doctor_name': filter_doctor_name
#     })


@login_required(login_url='/login')
def book_appointment(request):
  specialities = Specialty.objects.all()
  doctors = Doctors.objects.all()
  
  filter_speciality = request.GET.get('filter_speciality')
  filter_city = request.GET.get('filter_city')
  filter_doctor_name = request.GET.get('filter_doctor_name')

  if filter_speciality and filter_speciality != 'All':
    doctors = doctors.filter(specialty__name=filter_speciality)

  if filter_doctor_name:
    doctors = doctors.filter(user__first_name__icontains=filter_doctor_name)

  if filter_city:
    doctors = doctors.filter(user__id_address__city__icontains=filter_city)

  return render(request, "patients/book_appointment.html", {
    'doctors': doctors,
    'specialities': specialities,
    'filter_speciality': filter_speciality,
    'filter_doctor_name': filter_doctor_name,
    'filter_city': filter_city,
  })
  
  # return render(request,'patients/book_appointment.html',{"doctors":doctors})
from django.utils.timezone import make_aware
from datetime import date, datetime, time as dt_time, timedelta

@login_required(login_url='/login')
def patient_confirm_book(request, doctor):
    doctor_obj = get_object_or_404(Doctors, user__username=doctor)
    patient = get_object_or_404(Patients, user=request.user)
    times = Time.objects.all()

    today = datetime.today().date()

    if request.method == 'POST':
        date = request.POST.get("date")
        time_value = request.POST.get("time")
        description = request.POST.get("description")

        if not date or not time_value:
            messages.warning(request, "Please select both date and time.")
            return redirect(request.path)

        heure = Time.objects.get(time=time_value)

        # Check for slot already booked
        if Appointment.objects.filter(doctor=doctor_obj, start_date=date, time=heure).exists():
            messages.warning(request, "This time slot is already booked. Please choose another.")
            booked_times = Appointment.objects.filter(doctor=doctor_obj, start_date=date).values_list('time__time', flat=True)
            return render(request, 'patients/patient_confirm_book.html', {
                'doctor': doctor_obj,
                'times': times,
                'booked_times': [str(t) for t in booked_times],
                'message': "Slot already booked. Please choose another time.",
            })

        Appointment.objects.create(
            description=description,
            start_date=date,
            time=heure,
            doctor=doctor_obj,
            patient=patient
        )
        messages.success(request, "Appointment successfully booked.")
        return redirect('my_appointments')

    # GET Request
    booked_times = Appointment.objects.filter(doctor=doctor_obj, start_date=today).values_list('time__time', flat=True)
    existing_appointment = Appointment.objects.filter(patient=patient, doctor=doctor_obj, start_date=today).first()

    return render(request, 'patients/patient_confirm_book.html', {
        'doctor': doctor_obj,
        'times': times,
        'booked_times': [str(t) for t in booked_times],
        'existing_appointment': existing_appointment,
    })

@login_required
def my_appointments(request):
    try:
        patient = Patients.objects.get(user=request.user)
    except Patients.DoesNotExist:
        messages.error(request, "Patient profile not found.")
        return redirect('dashboard')

    appointments = Appointment.objects.filter(patient=patient).select_related(
        'doctor__user', 'time'
    ).prefetch_related('consultation__medications').order_by('-start_date', '-time__time')

    filter_date = request.GET.get('filter_date', '')
    filter_doctor_name = request.GET.get('filter_doctor_name', '')

    if filter_date:
        try:
            filter_date_obj = datetime.strptime(filter_date, '%Y-%m-%d').date()
            appointments = appointments.filter(start_date__date=filter_date_obj)
        except ValueError:
            messages.warning(request, "Invalid date format in filter.")

    if filter_doctor_name:
        appointments = appointments.filter(
            Q(doctor__user__first_name__icontains=filter_doctor_name) |
            Q(doctor__user__last_name__icontains=filter_doctor_name)
        )

    context = {
        'appointments': appointments,
        'filter_date': filter_date,
        'filter_doctor_name': filter_doctor_name,
        'total_appointments': appointments.count(),
    }

    return render(request, "patients/my_appointments.html", context)


@login_required
def view_prescription(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, patient__user=request.user)

    if not hasattr(appointment, 'consultation'):
        messages.error(request, "No prescription available yet for this appointment.")
        return redirect('my_appointments')  # Redirect to your appointment list

    context = {
        'appointment': appointment,
        'consultation': appointment.consultation,
        'medications': appointment.consultation.medications.all()
    }
    return render(request, 'patients/view_prescription.html', context)




from django.http import JsonResponse
from datetime import datetime
from django.utils import timezone


@login_required
def choose_consultation_time(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, patient__user=request.user)

    if request.method == 'POST':
        # Save the doctor's fee directly to the appointment amount (optional, already handled in model)
        appointment.amount = appointment.doctor.consult_fee
        appointment.save()
        return redirect('payment_view', appointment_id=appointment.id)

    return render(request, 'patients/consulta.html', {
        'appointment': appointment,
    })


@login_required
def payment_view(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, patient__user=request.user)

    if request.method == "POST":
        bkash_number = request.POST.get('bkash_number')

        # Validate bkash number server-side (optional but good practice)
        valid_prefixes = ['013', '015', '016', '017', '018', '019']
        if len(bkash_number) == 11 and bkash_number[:3] in valid_prefixes:
            appointment.payment_status = True
            appointment.save()

            messages.success(request, "Payment successful! Thank you.")
            return redirect('payment_success', appointment_id=appointment.id)
        else:
            messages.error(request, "Invalid Bkash number.")

    return render(request, 'patients/payment.html', {'appointment': appointment})


@login_required
def payment_success(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, patient__user=request.user)

    if not appointment.payment_status:
        messages.error(request, "You have not completed the payment yet.")
        return redirect('payment_view', appointment_id=appointment.id)

    return render(request, 'patients/payment_success.html', {'appointment': appointment})




def patient_appointment_report(request):
    patient = request.user.patient  # assuming OneToOne User → Patients relationship

    now = timezone.now()
    today = now.date()
    one_month_ago = today - timedelta(days=30)
    six_months_ago = today - timedelta(days=180)

    # All appointments of the patient
    all_appointments = Appointment.objects.filter(patient=patient)

    # Unique doctors the patient requested appointments from
    doctor_list = all_appointments.values_list('doctor__user__first_name', flat=True).distinct()

    # Appointments by time period only (no status filtering)
    appointments_today = all_appointments.filter(start_date__date=today)
    appointments_last_month = all_appointments.filter(start_date__date__gte=one_month_ago)
    appointments_last_six_months = all_appointments.filter(start_date__date__gte=six_months_ago)

    context = {
        'total_appointments': all_appointments.count(),
        'doctor_list': doctor_list,
        'appointments_today': appointments_today,
        'appointments_last_month': appointments_last_month,
        'appointments_last_six_months': appointments_last_six_months,
    }

    return render(request, 'patients/report.html', context)