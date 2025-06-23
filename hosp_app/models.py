from django.db import models

# Create your models here.
class Hosp(models.Model):
    name=models.CharField(max_length=100)
    address=models.CharField(max_length=100)
    dist=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    contact=models.CharField(max_length=100)
    loginid=models.ForeignKey('Login',on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Login(models.Model):
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=50)
    usertype=models.CharField(max_length=100)
    status=models.IntegerField(default=0)

import random
import string
from django.db import models

class Patient(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    age = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    loginid = models.ForeignKey(Login, on_delete=models.CASCADE)

    pr_number = models.CharField(max_length=15, unique=True, blank=True, null=True) 
    def save(self, *args, **kwargs):
        if not self.pr_number:  
            last_patient = Patient.objects.order_by("-id").first()  
            last_number = int(last_patient.pr_number[3:]) if last_patient and last_patient.pr_number else 1000
            alphabet_prefix = ''.join(random.choices(string.ascii_uppercase, k=3)) 
            self.pr_number = f"{alphabet_prefix}{last_number + 1}"  

        super().save(*args, **kwargs) 

class Doctor(models.Model):
    uploaded_image = models.ImageField(upload_to='images/', blank=True, null=True)
    name=models.CharField(max_length=100)
    gender=models.CharField(max_length=100)
    age=models.CharField(max_length=100)
    specification=models.CharField(max_length=100)
    exp=models.CharField(max_length=100)
    qualif=models.CharField(max_length=100)
    contact=models.CharField(max_length=100)
    con_fee=models.CharField(max_length=100)
    hosp_name=models.ForeignKey(Hosp,on_delete=models.CASCADE)
    loginid=models.ForeignKey('Login',on_delete=models.CASCADE)

class Appointment(models.Model):
    pat_id=models.ForeignKey(Patient,on_delete=models.CASCADE)
    doc_id=models.ForeignKey(Doctor,on_delete=models.CASCADE)
    hosp_id=models.ForeignKey(Hosp,on_delete=models.CASCADE)
    book_date=models.DateField()
    book_time=models.TimeField()
    cancel=models.CharField(max_length=100)
    appointment_type = models.CharField(max_length=10,choices=[("Online", "Online"), ("Offline", "Offline")],blank=True,null=True)
    pres = models.CharField(max_length=100, blank=True, null=True)
    curr_date=models.DateTimeField(auto_now_add=True)
    url=models.CharField(max_length=100,null=True, blank=True)
    status=models.IntegerField(default=0,null=True, blank=True) 


class Prescription(models.Model):
    appointment = models.ForeignKey(Appointment, related_name="prescriptions", on_delete=models.CASCADE)
    medicine_name = models.CharField(max_length=100)
    time_of_day = models.CharField(max_length=50)  # Stores selections as comma-separated values
    before_or_after_food = models.CharField(max_length=10, choices=[("Before", "Before Food"), ("After", "After Food")])
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.medicine_name} ({self.appointment.pat_id.name})"




class Payment(models.Model):
    app_id=models.ForeignKey(Appointment,on_delete=models.CASCADE,null=True)
    card_name=models.CharField(max_length=100)
    card_number=models.CharField(max_length=100)
    exp=models.CharField(max_length=100)
    cvv=models.CharField(max_length=100)
    amt=models.IntegerField(max_length=100)

class Lab(models.Model):
    hosp_id=models.ForeignKey(Hosp,on_delete=models.CASCADE)
    loc=models.CharField(max_length=100)
    name=models.CharField(max_length=100)
    loginid=models.ForeignKey('Login',on_delete=models.CASCADE)

class Labtest(models.Model):
    app_id = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    lab_id = models.ForeignKey(Lab, on_delete=models.CASCADE)
    curr_date = models.DateTimeField(auto_now_add=True)
    report_file = models.FileField(upload_to='lab_reports/', blank=True, null=True)  
    report_given = models.TextField(blank=True, null=True)
    test_details = models.CharField(max_length=100)
    status = models.IntegerField(default=0)  # 0 = Payment Pending, 1 = Paid
    card_name = models.CharField(max_length=100, blank=True, null=True)
    card_number = models.CharField(max_length=16, blank=True, null=True)
    exp_date = models.CharField(max_length=10, blank=True, null=True)
    cvv = models.CharField(max_length=3, blank=True, null=True)
    test_details = models.TextField()  
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  
    test_prices = models.JSONField(default=dict) 
    def total_cost(self):
        return sum(self.test_prices.values())

class Insurance(models.Model):
    
    inc_id=models.CharField(max_length=100)
    agent_name=models.CharField(max_length=100)
    contact=models.CharField(max_length=100)
    loginid=models.ForeignKey('Login',on_delete=models.CASCADE)

class Ins_taken(models.Model):
    
    category =models.CharField(max_length=100)
    scheme_name=models.CharField(max_length=100)
    details =models.CharField(max_length=100)
    type =models.CharField(max_length=100)
    amount=models.CharField(max_length=100)
    
class Ins_pat(models.Model):
    pat_id=models.ForeignKey(Patient,on_delete=models.CASCADE)
    hosp_id=models.ForeignKey(Hosp,on_delete=models.CASCADE)
    disease_name =models.CharField(max_length=100)
    doc_name=models.CharField(max_length=100)
    ins_num =models.CharField(max_length=100)
    details =models.CharField(max_length=100)
    curr_date=models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=0) 
    sa = models.IntegerField(default=0)  
    file = models.FileField(upload_to="hospital_notes/", blank=True, null=True)
    amt=models.CharField(max_length=100)
    ins_amt_status=models.IntegerField(default=0)




class Complaint(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)  # ✅ Links to logged-in patient
    subject = models.CharField(max_length=255)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)  # ✅ Stores submission time
    response = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Complaint by {self.patient.name} - {self.subject}"




class Donation(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    blood_group = models.CharField(max_length=3, choices=[
        ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')
    ])
    phone_number = models.CharField(max_length=15)
    organ_name = models.CharField(max_length=100)
    acknowledgment = models.FileField(upload_to="acknowledgments/")  # ✅ Stores file in "media/acknowledgments/"
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.organ_name}"



class Recipient(models.Model):
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    email = models.EmailField()
    blood_group = models.CharField(max_length=3, choices=[
        ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')
    ])
    organ_needed = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    submitted_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"{self.name} - Needs {self.organ_needed}"

class OrganMatch(models.Model):
    recipient = models.ForeignKey(Recipient, on_delete=models.CASCADE)
    donor = models.ForeignKey(Donation, on_delete=models.CASCADE)
    matched_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Match: {self.recipient.name} ↔ {self.donor.name}"



class TransferAppointment(models.Model):
    pat_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doc_id = models.ForeignKey(Doctor, on_delete=models.CASCADE)  # Current doctor
    transfer_doc_id = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="transferred_to")  # New doctor
    transfer_date = models.DateField(auto_now_add=True)
    class Meta:
        unique_together = ("pat_id", "transfer_doc_id") 
    def __str__(self):
        return f"{self.pat_id.name} transferred from {self.doc_id.name} to {self.transfer_doc_id.name}"
