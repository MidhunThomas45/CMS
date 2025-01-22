from django.contrib import admin
from .models import Bill, MedicalRecord, MedicineType, Staff, Department, Salary, Gender, Specialization, Doctor, Receptionist, TimeSlot, Schedule, Patient, Appointment, Token, Medicine, Prescription, Consultation
# Register your models here.
admin.site.register(Staff)
admin.site.register(Department)
admin.site.register(Salary)
admin.site.register(Gender)
admin.site.register(Specialization)
admin.site.register(Doctor)
admin.site.register(Receptionist)
admin.site.register(TimeSlot)
admin.site.register(Schedule)
admin.site.register(Patient)
admin.site.register(Appointment)
admin.site.register(Token)
admin.site.register(Medicine)
admin.site.register(Prescription)
admin.site.register(Consultation)
admin.site.register(MedicalRecord)
admin.site.register(Bill)
admin.site.register(MedicineType)

admin.site.register(MedicineType)