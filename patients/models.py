from django.db import models
from users.models import Patients ,Doctors
from django.utils import timezone
from datetime import timedelta

class Time(models.Model):
    time = models.CharField(max_length=20)
    duration_minutes = models.PositiveIntegerField()

    class Meta:
        verbose_name = "Time"
        verbose_name_plural = "Times"
    def __str__(self):
        return self.time


    def calculate_amount(self):
        # Example amount calculation based on duration
        return (self.duration_minutes // 15) * 1000

    def __str__(self):
        return f"{self.duration_minutes} minutes"
    
class Status(models.Model):
    status =  models.CharField(max_length=20) 
    class Meta:
        verbose_name = "Status"
        verbose_name_plural = "Status"
    def __str__(self):
        return self.status

class Appointment(models.Model):
    doctor = models.ForeignKey(Doctors, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patients, on_delete=models.CASCADE)
    description = models.TextField()
    start_date = models.DateTimeField()
    time = models.ForeignKey(Time, on_delete=models.CASCADE, default=1)
    payment_status = models.BooleanField(default=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Payment amount in Taka

    class Meta:
        verbose_name = "Appointment"
        verbose_name_plural = "Appointments"

    def __str__(self):
        return f"Appointment with Dr. {self.doctor.user.get_full_name()} on {self.start_date}"


class Consultation(models.Model):
    appointment = models.OneToOneField('Appointment', on_delete=models.CASCADE)
    diagnosis = models.TextField(blank=True)
    prescription_notes = models.TextField(blank=True)
    follow_up_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Consultation for {self.appointment.patient.user.get_full_name()}"


class Medication(models.Model):
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE, related_name='medications')
    name = models.CharField(max_length=100)
    dosage = models.CharField(max_length=50)
    frequency = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)
    instructions = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} - {self.dosage}"