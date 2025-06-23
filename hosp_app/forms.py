from django import forms
from .models import *

class Hospuser(forms.ModelForm):
    
    class Meta:
        model=Hosp
        fields=['name','address','dist','city','contact']

class Log(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model=Login
        fields=['email','password']

class Patuser(forms.ModelForm):
    
    class Meta:
        model=Patient
        fields=['name','address','gender','age','contact']


class Docuser(forms.ModelForm):
    hosp_name = forms.ModelChoiceField(queryset=Hosp.objects.all(), label='Select Hospital')

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Others', 'Others'),
    ]

    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        widget=forms.RadioSelect,
        label='Gender'
    )

    class Meta:
        model = Doctor
        fields = ['uploaded_image', 'name', 'gender', 'age', 'specification', 'exp', 'qualif', 'contact', 'hosp_name']

class DoctorFeeForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['con_fee']



class Labuser(forms.ModelForm):
    
    class Meta:
        model=Lab
        fields=['name','loc']

class Pat_login(forms.Form):
    email=forms.EmailField()
    password=forms.CharField(widget=forms.PasswordInput)
    
class EmailUpdate(forms.ModelForm):
   # password=forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model=Login
        fields=['email']


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['book_date', 'book_time']



class Pay_form(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['card_name', 'card_number','exp', 'cvv']


class PrescriptionForm(forms.ModelForm):
    time_of_day = forms.MultipleChoiceField(
        choices=[
    ("Morning & Evening", "Morning & Evening"),
    ("Morning Only", "Morning Only"),
    ("Evening Only", "Evening Only"),
    ("Morning, Afternoon & Evening", "Morning, Afternoon & Evening"),
    ("Morning & Afternoon", "Morning & Afternoon"),
    ("Afternoon & Evening", "Afternoon & Evening"),
    ("Night Only", "Night Only"),
    ("Morning, Afternoon, Evening & Night", "Morning, Afternoon, Evening & Night"),
],

        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Prescription
        fields = ['medicine_name', 'time_of_day', 'before_or_after_food', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

# class Labtestform(forms.ModelForm):
#     class Meta:
#         model = Labtest
#         fields = ['test_details']
class Labtestform(forms.ModelForm):
    TEST_CHOICES = [
        ('Blood Test', 'Blood Test - ₹500'),
        ('Urine Test', 'Urine Test - ₹400'),
        ('Diabetes Test', 'Diabetes Test - ₹600'),
        ('Infectious Disease Test', 'Infectious Disease Test - ₹800')
    ]
    
    selected_tests = forms.MultipleChoiceField(
        choices=TEST_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = Labtest
        fields = ['selected_tests']

class Labfileform(forms.ModelForm):
    class Meta:
        model = Labtest
        fields = ['report_file']


class Incuser(forms.ModelForm):
    class Meta:
        model=Insurance
        fields=['inc_id','agent_name','contact']



class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['subject', 'message']
        widgets = {
            'subject': forms.TextInput(attrs={'placeholder': 'Enter subject here', 'class': 'form-control'}),
            'message': forms.Textarea(attrs={'placeholder': 'Write your complaint...', 'class': 'form-control'}),
        }

class ResponseForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['response']
        widgets = {
            'response': forms.Textarea(attrs={'placeholder': 'Write your response...', 'class': 'form-control'}),
        }



class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['name', 'address', 'blood_group', 'phone_number', 'organ_name', 'acknowledgment']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter full name', 'class': 'form-control'}),
            'address': forms.Textarea(attrs={'placeholder': 'Enter your address', 'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Enter phone number', 'class': 'form-control'}),
            'organ_name': forms.TextInput(attrs={'placeholder': 'Enter organ name', 'class': 'form-control'}),
            'acknowledgment': forms.FileInput(attrs={'class': 'form-control'}),
        }


class RecipientForm(forms.ModelForm):
    class Meta:
        model = Recipient
        fields = ['name', 'contact', 'email', 'blood_group', 'organ_needed', 'location']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter full name', 'class': 'form-control'}),
            'contact': forms.TextInput(attrs={'placeholder': 'Enter contact number', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter email', 'class': 'form-control'}),
            'blood_group': forms.Select(attrs={'class': 'form-control'}),
            'organ_needed': forms.TextInput(attrs={'placeholder': 'Enter required organ', 'class': 'form-control'}),
            'location': forms.TextInput(attrs={'placeholder': 'Enter location', 'class': 'form-control'}),
        }


class xrayform(forms.Form):
    Image=forms.ImageField()