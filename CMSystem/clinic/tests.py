from django.test import TestCase
from datetime import date, datetime, time
from django.contrib.auth import get_user_model
from .models import (
    Department, Salary, Gender, Staff, Specialization, Doctor, Receptionist,
    TimeSlot, Schedule, Patient, Appointment, Token, MedicineType, Medicine,
    Prescription, Consultation, MedicalRecord, Bill
)

class ModelsTestCase(TestCase):
    def setUp(self):
        # Create Gender
        self.gender = Gender.objects.create(name="Male")
        
        # Create Department
        self.department = Department.objects.create(department_name="Cardiology")
        
        # Create Staff
        self.staff = get_user_model().objects.create_user(
            username="doctor1",
            first_name="John",
            last_name="Doe",
            password="test123",
            gender=self.gender,
            mobile_number="1234567890",
            dob=datetime(1985, 5, 15),
            department=self.department
        )
        
        # Create Specialization
        self.specialization = Specialization.objects.create(specialization_name="Cardiologist")
        
        # Create Doctor
        self.doctor = Doctor.objects.create(
            staff=self.staff,
            specialization=self.specialization,
            consultation_fee=500.00,
            year_of_experience=10
        )
        
        # Create Patient
        self.patient = Patient.objects.create(
            full_name="Jane Doe",
            dob=date(1990, 7, 20),
            gender=self.gender,
            mobile_number="9876543210",
            address="123 Main Street"
        )
        
        # Create Salary
        self.salary = Salary.objects.create(
            staff=self.staff,
            base_salary=50000.00,
            deductions=2000.00,
            increment=5000.00,
            salary_payment_date=date(2024, 1, 1)
        )
        
        # Create TimeSlot
        self.time_slot = TimeSlot.objects.create(start_time=time(9, 0), end_time=time(10, 0))
        
        # Create Schedule
        self.schedule = Schedule.objects.create(
            doctor=self.doctor,
            schedule_date=date(2024, 1, 20),
            token=1
        )
        self.schedule.time_slot.add(self.time_slot)
        
        # Create Appointment
        self.appointment = Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            schedule=self.schedule,
            appointment_date=date(2024, 1, 20),
            is_pre_booked=True
        )
        
        # Create Token
        self.token = Token.objects.create(
            appointment=self.appointment,
            token_number=1
        )
        
        # Create MedicineType and Medicine
        self.medicine_type = MedicineType.objects.create(type_name="Tablet")
        self.medicine = Medicine.objects.create(
            name="Paracetamol",
            dose="500mg",
            type=self.medicine_type
        )
        
        # Create Prescription
        self.prescription = Prescription.objects.create(
            dosage=2,
            frequency=3,
            duration=5,
            patient=self.patient
        )
        self.prescription.medicines.add(self.medicine)
        
        # Create Consultation
        self.consultation = Consultation.objects.create(
            token=self.token,
            patient=self.patient,
            symptoms="Fever and headache",
            diagnosis="Flu",
            notes="Rest and drink fluids",
            additional_notes="Follow-up in a week",
            created_at=datetime(2024, 1, 20, 10, 0),
            prescription=self.prescription
        )
        
        # Create MedicalRecord
        self.medical_record = MedicalRecord.objects.create(
            patient=self.patient,
            record_date=date(2024, 1, 20),
            consultation=self.consultation
        )
        self.medical_record.doctors.add(self.doctor)
        
        # Create Bill
        self.bill = Bill.objects.create(
            appointment=self.appointment,
            total_amount=1000.00,
            payment_status=True
        )

    def test_gender_str(self):
        self.assertEqual(str(self.gender), "Male")
        
    def test_department_str(self):
        self.assertEqual(str(self.department), "Cardiology")
        
    def test_specialization_str(self):
        self.assertEqual(str(self.specialization), "Cardiologist")
        
    def test_doctor_str(self):
        self.assertEqual(str(self.doctor), "Dr. John Doe")
        
    def test_patient_str(self):
        self.assertEqual(str(self.patient), "Jane Doe")
        
    def test_salary_calculation(self):
        self.assertEqual(self.salary.total_salary, 53000.00)
        
    def test_schedule_association(self):
        self.assertEqual(self.schedule.doctor, self.doctor)
        self.assertIn(self.time_slot, self.schedule.time_slot.all())
        
    def test_token_creation(self):
        self.assertEqual(self.token.token_number, 1)
        
    def test_appointment_association(self):
        self.assertEqual(self.appointment.patient, self.patient)
        self.assertEqual(self.appointment.doctor, self.doctor)
        
    def test_medicine_str(self):
        self.assertEqual(str(self.medicine), "Paracetamol")
        
    def test_prescription_medicines(self):
        self.assertIn(self.medicine, self.prescription.medicines.all())
        
    def test_consultation_details(self):
        self.assertEqual(self.consultation.symptoms, "Fever and headache")
        self.assertEqual(self.consultation.diagnosis, "Flu")
        
    def test_medical_record_association(self):
        self.assertIn(self.doctor, self.medical_record.doctors.all())
        
    def test_bill_creation(self):
        self.assertEqual(self.bill.total_amount, 1000.00)
        self.assertTrue(self.bill.payment_status)
