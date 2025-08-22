from django.contrib import admin

# Register your models here.
from .models import Users, Address, Doctors, Patients, Specialty

admin.site.register(Address)
admin.site.register(Users)
admin.site.register(Patients)
admin.site.register(Specialty)



# @admin.register(Doctors)
# class DoctorsAdmin(admin.ModelAdmin):
#     list_display = ['username']


@admin.register(Doctors)
class DoctorsAdmin(admin.ModelAdmin):
    list_display = [
        'user',            # shows the __str__ of the user (usually username or email)
        'specialty',
        'bio',
        'get_email',
        'get_gender',
        'get_birthday',
        'get_is_doctor'
    ]

    def get_email(self, obj):
        return obj.user.email

    def get_gender(self, obj):
        return obj.user.gender

    def get_birthday(self, obj):
        return obj.user.birthday

    def get_is_doctor(self, obj):
        return obj.user.is_doctor