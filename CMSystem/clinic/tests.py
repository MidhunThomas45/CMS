from django.test import TestCase
from django.utils import timezone
from .models import (
    Department, Gender, Staff, Specialization, Doctor, Receptionist,
    TimeSlot, Schedule, Patient, Appointment, Token, MedicineType,
    Medicine, Prescription, Consultation, MedicalRecord, Bill
)

class HealthcareModelTestCase(TestCase):

    def setUp(self):
        # Setting up some initial data for testing
        self.department = Department.objects.create(department_name='Cardiology', base_salary=5000.00)
        self.gender_male = Gender.objects.create(name='Male')
        self.gender_female = Gender.objects.create(name='Female')
        self.staff_member = Staff.objects.create(
            username='john_doe', first_name='John', last_name='Doe',
            gender=self.gender_male, mobile_number='1234567890',
            joining_date=timezone.now(), department=self.department
        )
        self.specialization = Specialization.objects.create(specialization_name='Cardiologist')
        self.doctor = Doctor.objects.create(
            staff=self.staff_member, specialization=self.specialization,
            consultation_fee=1000.00, year_of_experience=5
        )
        self.receptionist = Receptionist.objects.create(staff=self.staff_member, year_of_experience=2)
        self.time_slot = TimeSlot.objects.create(start_time='09:00:00', end_time='12:00:00')
        self.patient = Patient.objects.create(
            full_name='Jane Doe', dob='1990-01-01',
            gender=self.gender_female, mobile_number='9876543210', address='123 Elm St.'
        )
        self.appointment = Appointment.objects.create(
            patient=self.patient, doctor=self.doctor,
            appointment_date='2025-01-22', is_pre_booked=True
        )
        self.token = Token.objects.create(appointment=self.appointment, token_number=1)
        self.medicine_type = MedicineType.objects.create(type_name='Tablet')
        self.medicine = Medicine.objects.create(name='Aspirin', dose='500mg', type=self.medicine_type)
        self.prescription = Prescription.objects.create(
            patient=self.patient, dosage=1, frequency=2, duration=5
        )
        self.prescription.medicines.add(self.medicine)
        self.consultation = Consultation.objects.create(
            token=self.token, patient=self.patient,
            symptoms='Chest pain', diagnosis='Heartburn', notes='Patient stable',
            additional_notes='No immediate concerns', created_at=timezone.now(),
            prescription=self.prescription
        )
        self.medical_record = MedicalRecord.objects.create(
            patient=self.patient, record_date=timezone.now(),
            consultation=self.consultation
        )
        self.medical_record.doctors.add(self.doctor)
        self.bill = Bill.objects.create(appointment=self.appointment, total_amount=1500.00)

    def test_department_creation(self):
        self.assertEqual(self.department.department_name, 'Cardiology')
        self.assertEqual(self.department.base_salary, 5000.00)

    def test_gender_creation(self):
        self.assertEqual(self.gender_male.name, 'Male')
        self.assertEqual(self.gender_female.name, 'Female')

    def test_staff_creation(self):
        self.assertEqual(self.staff_member.username, 'john_doe')
        self.assertEqual(self.staff_member.first_name, 'John')
        self.assertEqual(self.staff_member.last_name, 'Doe')

    def test_doctor_creation(self):
        self.assertEqual(self.doctor.staff.first_name, 'John')
        self.assertEqual(self.doctor.specialization.specialization_name, 'Cardiologist')

    def test_receptionist_creation(self):
        self.assertEqual(self.receptionist.staff.first_name, 'John')
        self.assertEqual(self.receptionist.year_of_experience, 2)

    def test_time_slot_creation(self):
        self.assertEqual(self.time_slot.start_time, '09:00:00')
        self.assertEqual(self.time_slot.end_time, '12:00:00')

    def test_patient_creation(self):
        self.assertEqual(self.patient.full_name, 'Jane Doe')
        self.assertEqual(self.patient.address, '123 Elm St.')

    def test_appointment_creation(self):
        self.assertEqual(self.appointment.patient.full_name, 'Jane Doe')
        self.assertEqual(self.appointment.is_pre_booked, True)

    def test_token_creation(self):
        self.assertEqual(self.token.token_number, 1)
        self.assertTrue(self.token.status)

    def test_medicine_creation(self):
        self.assertEqual(self.medicine.name, 'Aspirin')
        self.assertEqual(self.medicine.dose, '500mg')

    def test_prescription_creation(self):
        self.assertEqual(self.prescription.dosage, 1)
        self.assertEqual(self.prescription.frequency, 2)

    def test_consultation_creation(self):
        self.assertEqual(self.consultation.symptoms, 'Chest pain')
        self.assertEqual(self.consultation.diagnosis, 'Heartburn')

    def test_medical_record_creation(self):
        self.assertEqual(self.medical_record.patient.full_name, 'Jane Doe')
        self.assertEqual(self.medical_record.consultation.diagnosis, 'Heartburn')

    def test_bill_creation(self):
        self.assertEqual(self.bill.total_amount, 1500.00)
        self.assertFalse(self.bill.payment_status)

    def test_list_staff(self):
        # List all staff members
        staff_list = Staff.objects.all()
        self.assertEqual(len(staff_list), 1)
        self.assertEqual(staff_list[0].first_name, 'John')

    def test_list_doctors(self):
        # List all doctors
        doctors_list = Doctor.objects.all()
        self.assertEqual(len(doctors_list), 1)
        self.assertEqual(doctors_list[0].staff.first_name, 'John')

    def test_update_patient(self):
        # Update patient details
        self.patient.address = '456 Maple Ave'
        self.patient.mobile_number = '1231231234'
        self.patient.save()

        updated_patient = Patient.objects.get(id=self.patient.id)
        self.assertEqual(updated_patient.address, '456 Maple Ave')
        self.assertEqual(updated_patient.mobile_number, '1231231234')

    def test_delete_medicine(self):
        # Delete a medicine
        medicine_id = self.medicine.id
        self.medicine.delete()
        
        with self.assertRaises(Medicine.DoesNotExist):
            Medicine.objects.get(id=medicine_id)

    def tearDown(self):
        self.department.delete()
        self.gender_male.delete()
        self.gender_female.delete()
        self.staff_member.delete()
        self.specialization.delete()
        self.doctor.delete()
        self.receptionist.delete()
        self.time_slot.delete()
        self.patient.delete()
        self.appointment.delete()
        self.token.delete()
        self.medicine_type.delete()
        self.prescription.delete()
        self.consultation.delete()
        self.medical_record.delete()
        self.bill.delete()
