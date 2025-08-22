from django.contrib import admin

from .models import Appointment, Time,Consultation,Medication


admin.site.register(Time)

admin.site.register(Consultation)
admin.site.register(Medication)


@admin.register(Appointment)
class AppointAdmin(admin.ModelAdmin):
    list_display = ['id','doctor','patient', 'description','start_date']


