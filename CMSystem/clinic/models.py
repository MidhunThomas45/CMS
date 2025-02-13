from django.db import models
from django.contrib.auth.models import AbstractUser

class Department(models.Model):
    department_name = models.CharField(max_length=50)
    base_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    def __str__(self):
        return self.department_name

# Gender Model
class Gender(models.Model):
    name = models.CharField(max_length=10, unique=True)  # Example: 'Male', 'Female', 'Other'

    def __str__(self):
        return self.name

# Staff Model
class Staff(AbstractUser):
    gender = models.ForeignKey(Gender, on_delete=models.SET_NULL, null=True, blank=True, related_name='staff_gender')
    dob = models.DateField(null=True, blank=True)
    mobile_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    joining_date = models.DateTimeField(null=True, blank=True)
    qualification = models.CharField(max_length=100, null=True, blank=True)
    photo = models.ImageField(upload_to='staff_photos/', null=True, blank=True) 
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='staff_department', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Salary(models.Model):
    staff = models.ForeignKey(
        Staff, on_delete=models.CASCADE, related_name='staff_salary', null=True, blank=True
    )
    base_salary = models.DecimalField(
        max_digits=10, decimal_places=2, null=True
    )
    deductions = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.0
    )
    increment = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.0
    )
    total_salary = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    payment_status = models.BooleanField(default=False)
    salary_payment_date = models.DateField()
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.base_salary is not None:
            self.total_salary = self.base_salary + self.increment - self.deductions
        else:
            self.total_salary = None
        super(Salary, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.staff.first_name if self.staff else 'Staff'}"

# class Salary(models.Model):
#     staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='staff_salary', null=True, blank=True)
#     base_salary = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='staff')
#     deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
#     increment = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
#     total_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
#     payment_status = models.BooleanField(default=False)
#     salary_payment_date = models.DateField()
#     updated_at = models.DateTimeField(auto_now=True)

#     def save(self, *args, **kwargs):
#         # Calculate total salary automatically before saving
#         if self.staff and self.staff.department:
#             self.base_salary = self.staff.department.base_salary  # Corrected here
#         self.total_salary = self.base_salary + self.increment - self.deductions
#         super(Salary, self).save(*args, **kwargs)

#     def get_base_salary(self):
#         return self.base_salary.salary

#     def __str__(self):
#         return f"{self.staff}"
    
# Specialization Table
class Specialization(models.Model):
    specialization_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.specialization_name

# Doctor Table
class Doctor(models.Model):
    staff = models.OneToOneField(Staff, on_delete=models.CASCADE, related_name='doctor')
    specialization = models.ForeignKey(Specialization, on_delete=models.CASCADE, related_name='doctors')
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2)
    year_of_experience = models.IntegerField()

    def __str__(self):
        return f"Dr. {self.staff.first_name} {self.staff.last_name}"  # Display staff name
    
# Receptionist Table
class Receptionist(models.Model):
    staff = models.OneToOneField(Staff, on_delete=models.CASCADE, related_name='receptionist')
    year_of_experience = models.IntegerField()

    def __str__(self):
        return f"{self.staff.first_name}"


class TimeSlot(models.Model):
    type = models.CharField(max_length=15, null=True, blank=True)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.type}"


# Schedule Table
class Schedule(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='schedules')
    schedule_date = models.DateField()
    time_slot = models.ManyToManyField(TimeSlot, related_name="schedules")
    token = models.IntegerField()
    status = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.doctor.staff.first_name}-{self.time_slot}"


# Patient Table
class Patient(models.Model):
    full_name = models.CharField(max_length=100)
    dob = models.DateField()
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE, related_name='patients')
    mobile_number = models.CharField(max_length=15)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.full_name

# Appointment Table
class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments_patient')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name='schedules', null=True, blank=True)
    appointment_date = models.DateField()
    is_pre_booked = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.patient.full_name}"

# Token Table
class Token(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='tokens')
    token_number = models.IntegerField()
    issued_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.appointment.patient.full_name}"


# Medicine Type
class MedicineType(models.Model):
    type_name = models.CharField(max_length=15)

    def __str__(self):
        return self.type_name

# Medicine Table
class Medicine(models.Model):
    name = models.CharField(max_length=50)
    dose = models.CharField(max_length=50)
    type = models.ForeignKey(MedicineType, on_delete=models.CASCADE, related_name='medicine_type')

    def __str__(self):
        return self.name

# Prescription Table
class Prescription(models.Model):
    medicines = models.ManyToManyField(Medicine, related_name='prescriptions')
    dosage = models.CharField(max_length=100)
    frequency = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='prescriptions')

    def __str__(self):
        return f"{self.patient.full_name}"

# Consultation Table
class Consultation(models.Model):
    token = models.ForeignKey(Token, on_delete=models.CASCADE, related_name='consultations')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='consultations')
    symptoms = models.TextField()
    diagnosis = models.CharField(max_length=50)
    notes = models.TextField()
    additional_notes = models.TextField()
    created_at = models.DateTimeField()
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE, related_name='consultations')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.patient.full_name}"

# Medical Record Table
class MedicalRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medical_records')
    doctors = models.ManyToManyField(Doctor, related_name='medical_records')
    record_date = models.DateField()
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE, related_name='medical_records')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.patient.full_name}"

# Bill Table
class Bill(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='bills')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
