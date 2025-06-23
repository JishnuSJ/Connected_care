
from django.contrib import messages
from django.shortcuts import render,redirect,get_object_or_404
from django.http import JsonResponse
import json
from .forms import *
from django.db.models import Q
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from hosp_app.models import Labtest
# Create your views here.
from .utils import *

def admin_mod(request):
    
    total_patients = Patient.objects.count()
    total_doctors = Doctor.objects.count()
    insurance_requested = Ins_pat.objects.count()
    insurance_approved = Ins_pat.objects.filter(status=1).count()


    doc_show = Doctor.objects.all()  
    hospitals = Hosp.objects.order_by("-id")[:3] 
    pat = Appointment.objects.order_by("-id")[:7] 
    doc = Doctor.objects.order_by("-id")[:7] 
    return render(request, "admin_main.html", {
        "total_patients": total_patients,
        "total_doctors": total_doctors,
        "insurance_requested": insurance_requested,
        "insurance_approved": insurance_approved,
        "doc_show": doc_show,
        "hospitals": hospitals,
        "pat":pat,
        "doc":doc 
    })



def doc_mod(request):
    user_id = request.session.get('user_id')  
    doc_data=get_object_or_404(Doctor,loginid=user_id)
    return render(request,'doc_main1.html',{"doc_data":doc_data})

def pat_mod(request):
    return render(request,'pathome.html')

def index(request):
    return render(request,'index.html')

def hosp_mod(request):
    user_id = request.session.get('user_id')  
    hosp = get_object_or_404(Hosp, loginid=user_id)  


    total_patients = Patient.objects.filter(appointment__hosp_id=hosp).count()  
    total_doctors = Doctor.objects.filter(hosp_name=hosp).count()
    insurance_requested = Ins_pat.objects.filter(hosp_id=hosp).count()
    insurance_approved = Ins_pat.objects.filter(hosp_id=hosp, status=1).count()
    notifications_list = Ins_pat.objects.filter(ins_amt_status=1).order_by("-id")[:4]
    latest_appointments = Appointment.objects.filter(status=1).order_by("-book_date")[:4] 
    doc_show = Doctor.objects.filter(hosp_name=hosp)  

    return render(request, "hosp_admin.html", {
        "total_patients": total_patients,
        "total_doctors": total_doctors,
        "insurance_requested": insurance_requested,
        "insurance_approved": insurance_approved,
        "doc_show": doc_show,
        "hospital_name": hosp.name,
        "notifications_list": notifications_list,
        "latest_appointments":latest_appointments
    })

    
def reg_hosp(request):
    if request.method=='POST':
        form=Hospuser(request.POST)
        form1=Log(request.POST)
        if form.is_valid() & form1.is_valid():
            f=form1.save(commit=False)
            f.usertype="hospital"
            f.save()

            f1=form.save(commit=False)
            f1.loginid=f
            f1.save()
            return redirect('/')
    else:
            form=Hospuser()
            form1=Log()
            
    return render(request,'reg_hosp.html',{'form':form,'form1':form1})

def reg_pat(request):
     

    if request.method=='POST':
        form=Patuser(request.POST)
        form1=Log(request.POST)
        if form.is_valid() & form1.is_valid():
            f=form1.save(commit=False)
            f.usertype="patient"
            f.status=1
            f.save()

            f1=form.save(commit=False)
            f1.loginid=f
            f1.save()
            return redirect('/')
    else:
            form=Patuser()
            form1=Log()
            
    return render(request,'reg_pat.html',{'form':form,'form1':form1})

def doc_reg(request):
    if request.method=='POST':
        form=Docuser(request.POST,request.FILES)
        form1=Log(request.POST)
        if form.is_valid() & form1.is_valid():
            f=form1.save(commit=False)
            f.usertype="doctor"
            f.save()

            f1=form.save(commit=False)
            f1.loginid=f
            f1.save()
            return redirect('/')
    else:
            form=Docuser()
            form1=Log()
            
    return render(request,'doc_reg.html',{'form':form,'form1':form1})

def hosp_reg_show(request):
    if 'user_id' in request.session:

        hosp_show=Hosp.objects.all()
        return render(request,'hosp_reg_show.html',{'hosp_show':hosp_show})
    else:
        return redirect('login')
   
def doc_reg_show(request):
    if 'user_id' in request.session:
        doc_show=Doctor.objects.all()
        return render(request,'doc_reg_show.html',{'doc_show':doc_show})
    else:
        return redirect('login')
def pat_reg_show(request):
    if 'user_id' in request.session:
        pat_show=Patient.objects.all()
        return render(request,'pat_reg_show.html',{'pat_show':pat_show})
    else:
        return redirect('login')
def approve(request,id):
     a=get_object_or_404(Login,id=id)
     a.status=1
     a.save()
     return redirect('admin_mod')
    
def reject(request,id):
     a=get_object_or_404(Login,id=id)
     a.status=2
     a.save()
     return redirect('admin_mod')

def login(request):
    
    if request.method=='POST':
         
        form=Pat_login(request.POST)
        print(form)
        if form.is_valid():
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
            if email == "admin@g.com" and password == "1":
                request.session['user_id'] = "admin"
                return redirect('admin_mod')
            try:
                user=Login.objects.get(email=email)
                if user.password==password and user.usertype=='patient' and user.status==1:
                    request.session['user_id']=user.id
                    return redirect('pat_mod')
                elif user.password==password and user.usertype=='doctor' and user.status==1:
                    request.session['user_id']=user.id
                    return redirect('doc_mod')
                elif user.password==password and user.usertype=='hospital' and user.status==1:
                    request.session['user_id']=user.id
                    return redirect('hosp_mod')
                elif user.password==password and user.usertype=='insurance' and user.status==1:
                    request.session['user_id']=user.id
                    return redirect('inc_mod')
                elif user.password==password and user.usertype=='lab' and user.status==1:
                    request.session['user_id']=user.id
                    return redirect('lab_mod')
                else:
                    messages.error(request,'Invalid password')
            except Login.DoesNotExist:
                messages.error(request,'user does not exits')
    else:
        form=Pat_login()
    return render(request, 'login.html', {'form': form})
       
def doc_pro_edit(request):
    if 'user_id' in request.session:
        a=request.session.get('user_id')
        a1=get_object_or_404(Login,id=a)
        logindata=get_object_or_404(Login,id=a1.id)
        doc_data=get_object_or_404(Doctor,loginid=a1)
        if request.method=='POST':
            form=Docuser(request.POST,request.FILES,instance=doc_data)
            form1=EmailUpdate(request.POST,instance=logindata)
            if form.is_valid() and form1.is_valid():
                form.save()
                form1.save()
                return redirect('doc_mod')
        else:
                form=Docuser(instance=doc_data)
                form1=EmailUpdate(instance=logindata)
        return render(request,'doc_pro_edit.html',{'form1':form,'form2':form1})
    else:
        return redirect('login')

def hosp_pro_edit(request):
    if 'user_id' in request.session:
        a=request.session.get('user_id')
        a1=get_object_or_404(Login,id=a)
        logindata=get_object_or_404(Login,id=a1.id)
        hos_data=get_object_or_404(Hosp,loginid=a1)
        if request.method=='POST':
            form=Hospuser(request.POST,request.FILES,instance=hos_data)
            form1=EmailUpdate(request.POST,instance=logindata)
            if form.is_valid() and form1.is_valid():
                form.save()
                form1.save()
                return redirect('hosp_mod')
        else:
                form=Hospuser(instance=hos_data)
                form1=EmailUpdate(instance=logindata)
        return render(request,'hosp_pro_edit.html',{'form1':form,'form2':form1})
    else:
        return redirect('login')


def pat_pro_edit(request):
    if 'user_id' in request.session:
        a=request.session.get('user_id')
        a1=get_object_or_404(Login,id=a)
        logindata=get_object_or_404(Login,id=a1.id)
        pat_data=get_object_or_404(Patient,loginid=a1)
        if request.method=='POST':
            form=Patuser(request.POST,request.FILES,instance=pat_data)
            form1=EmailUpdate(request.POST,instance=logindata)
            if form.is_valid() and form1.is_valid():
                form.save()
                form1.save()
                return redirect('pat_mod')
        else:
                form=Patuser(instance=pat_data)
                form1=EmailUpdate(instance=logindata)
        return render(request,'pat_pro_edit.html',{'form1':form,'form2':form1})
    else:
        return redirect('login')

def hosp_pat_show(request):
    if 'user_id' in request.session:
        hosp_show_pat=Hosp.objects.all()
        a=request.GET.get('search')
        if a:
             hosp_show_pat=Hosp.objects.filter(Q(name__icontains=a)|Q(dist__icontains=a)|Q(city__icontains=a))
        return render(request,'hosp_pat_show.html',{'hosp_show_pat':hosp_show_pat})
    else:
        return redirect('login')
    

def doc_pat_show(request,id):
    if 'user_id' in request.session:
        doc_show_pat=Doctor.objects.filter(hosp_name=id)
        return render(request,'doc_pat_show.html',{'doc_show_pat':doc_show_pat,'hospid':id})
    else:
        return redirect('login')
    


# from datetime import datetime, timedelta
# from django.shortcuts import render, get_object_or_404, redirect
# from .models import Appointment, Patient, Hosp, Doctor
# from .forms import AppointmentForm
# from django.core.serializers.json import DjangoJSONEncoder
# import json

# def pat_appointment_date(request, id, hosp_id):
#     if "user_id" in request.session:
#         user_id = request.session.get("user_id")  
#         patient_app = get_object_or_404(Patient, loginid=user_id)
#         hosp_appointment = get_object_or_404(Hosp, id=hosp_id)
#         doc_appointment = get_object_or_404(Doctor, id=id)

#         selected_date_raw = request.GET.get("book_date")  
#         selected_date = None
#         appointment_type = request.GET.get("appointment_type")
#         time_slots = []

#         if selected_date_raw:
#             try:
#                 selected_date = datetime.strptime(selected_date_raw, "%Y-%m-%d").date()  # ✅ Convert date format
#             except ValueError:
#                 selected_date = None 

#         if appointment_type == "Offline":
#             start_time, end_time = datetime.strptime("09:00", "%H:%M"), datetime.strptime("12:00", "%H:%M")
#         else:  # Online Appointment
#             start_time, end_time = datetime.strptime("18:00", "%H:%M"), datetime.strptime("19:00", "%H:%M")

#         while start_time < end_time:
#             time_slot = start_time.strftime("%H:%M")  
#             booked = Appointment.objects.filter(book_date=selected_date, book_time=time_slot).exists()  
#             time_slots.append({"time": time_slot, "booked": booked})  
#             start_time += timedelta(minutes=15)

#         if request.method == "POST":
#             form = AppointmentForm(request.POST)
#             selected_date = request.POST.get("book_date")
#             selected_time = request.POST.get("book_time")
#             selected_type = request.POST.get("appointment_type") 

#             try:
#                 selected_time = datetime.strptime(selected_time, "%H:%M").time()  # ✅ Convert strict format
#             except ValueError:
#                 return render(request, "pat_appointment_date.html", {
#                     "error": "Invalid time format. Please select a valid time slot.",
#                     "hosp_appointment": hosp_appointment,
#                     "doc_appointment": doc_appointment,
#                     "form": form,
#                     "time_slots": time_slots,
#                 })

#             existing_appointment = Appointment.objects.filter(book_date=selected_date, book_time=selected_time).exists()

#             if existing_appointment:
#                 return render(request, "pat_appointment_date.html", {
#                     "error": f"The time slot {selected_time} on {selected_date} is already booked.",
#                     "hosp_appointment": hosp_appointment,
#                     "doc_appointment": doc_appointment,
#                     "form": form,
#                     "time_slots": time_slots,
#                 })
#             else:
#                 appointment = form.save(commit=False)
#                 appointment.pat_id = patient_app
#                 appointment.doc_id = doc_appointment
#                 appointment.hosp_id = hosp_appointment
#                 appointment.appointment_type = selected_type
#                 appointment.status = 1
#                 appointment.save()
#                 return redirect("pat_payment", id=appointment.id)

#         return render(request, "pat_appointment_date.html", {
#             "hosp_appointment": hosp_appointment,
#             "doc_appointment": doc_appointment,
#             "time_slots": time_slots,
#             "selected_date": selected_date,
#             "booked_slots_json": json.dumps(time_slots, cls=DjangoJSONEncoder),
#         })
    
#     return redirect("login")

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from datetime import datetime, timedelta

def pat_appointment_date(request, id, hosp_id):
    if "user_id" not in request.session:
        return redirect("login")

    user_id = request.session["user_id"]
    patient_app = get_object_or_404(Patient, loginid=user_id)
    hosp_appointment = get_object_or_404(Hosp, id=hosp_id)
    doc_appointment = get_object_or_404(Doctor, id=id)

    # AJAX request for time slots
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        selected_date_raw = request.GET.get("date")
        appointment_type = request.GET.get("appointment_type")

        try:
            selected_date = datetime.strptime(selected_date_raw, "%Y-%m-%d").date()
        except (ValueError, TypeError):
            return JsonResponse({"error": "Invalid date"}, status=400)

        if appointment_type == "Offline":
            start_time = datetime.strptime("09:00", "%H:%M")
            end_time = datetime.strptime("12:00", "%H:%M")
        else:
            start_time = datetime.strptime("18:00", "%H:%M")
            end_time = datetime.strptime("19:00", "%H:%M")

        time_slots = []
        while start_time < end_time:
            time_slot = start_time.strftime("%H:%M")
            is_booked = Appointment.objects.filter(
                book_date=selected_date,
                book_time=time_slot,
                doc_id=doc_appointment
            ).exists()
            time_slots.append({"time": time_slot, "booked": is_booked})
            start_time += timedelta(minutes=15)

        return JsonResponse({"time_slots": time_slots})

    # Handle form POST
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        selected_date = request.POST.get("book_date")
        selected_time = request.POST.get("book_time")
        selected_type = request.POST.get("appointment_type")

        try:
            selected_time_obj = datetime.strptime(selected_time, "%H:%M").time()
        except ValueError:
            return render(request, "pat_appointment_date.html", {
                "error": "Invalid time format.",
                "hosp_appointment": hosp_appointment,
                "doc_appointment": doc_appointment,
            })

        existing = Appointment.objects.filter(
            book_date=selected_date,
            book_time=selected_time_obj,
            doc_id=doc_appointment
        ).exists()

        if existing:
            return render(request, "pat_appointment_date.html", {
                "error": f"The time slot {selected_time} on {selected_date} is already booked.",
                "hosp_appointment": hosp_appointment,
                "doc_appointment": doc_appointment,
            })

        appointment = form.save(commit=False)
        appointment.pat_id = patient_app
        appointment.doc_id = doc_appointment
        appointment.hosp_id = hosp_appointment
        appointment.appointment_type = selected_type
        appointment.status = 1
        appointment.save()
        return redirect("pat_payment", id=appointment.id)

    return render(request, "pat_appointment_date.html", {
        "hosp_appointment": hosp_appointment,
        "doc_appointment": doc_appointment,
    })


def pat_appointment_show(request):
    if 'user_id' in request.session:
        a = request.session.get('user_id') 
        pat = get_object_or_404(Patient, loginid=a)
        appointment_show = Appointment.objects.filter(pat_id=pat,status=1)
        return render(request, 'pat_appointment_show.html', {'appointment_show': appointment_show})
    else:
        return redirect('login')

def cancel_appa(request,id):
     a=get_object_or_404(Appointment,id=id)
     a.status=1
     a.save()
     return redirect('pat_mod')

def pat_appoint_show_admin(request):
    appointment_shown = Appointment.objects.all()
    return render(request, 'pat_appoint_show_admin.html', {'appointment_shown': appointment_shown})





def pat_payment(request, id):
    if 'user_id' in request.session:
        app_id = get_object_or_404(Appointment, id=id)  
        con_fee = app_id.doc_id.con_fee

        if request.method == 'POST':
            form = Pay_form(request.POST)  
            if form.is_valid():
                payment = form.save(commit=False)
                payment.app_id = app_id
                payment.amt = con_fee   
                payment.save()

                # ✅ Generate PDF after payment
                return generate_appointment_pdf(request, app_id.id)  
        else:     
            form = Pay_form()

        return render(request, 'pat_payment.html', {'form': form, 'amount': con_fee})
    else:
        return redirect('login')

from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO
from .models import Appointment

def generate_appointment_pdf(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    patient = appointment.pat_id
    doctor = appointment.doc_id
    hospital = appointment.hosp_id

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="Appointment_{appointment.id}.pdf"'

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # ---------- HEADER ----------
    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, height - 50, f"{hospital.name.upper()}")

    p.setFont("Helvetica", 11)
    p.drawString(200, height - 65, f"{hospital.address}, {hospital.city}, {hospital.dist}")
    p.setFont("Helvetica-Bold", 12)
    p.drawString(240, height - 85, "APPOINTMENT SLIP")

    # ---------- APPOINTMENT ID ----------
    p.setFont("Helvetica", 10)
    p.drawString(450, height - 70, "Appointment ID:")
    p.setFont("Helvetica-Bold", 11)
    p.drawString(450, height - 85, f"{appointment.id:08d}")

    # ---------- BLOCK: DETAILS ----------
    y = height - 130
    p.setFont("Helvetica", 11)

    fields = [
        ("Hospital", hospital.name),
        ("Doctor", f"{doctor.name} ({doctor.specification})"),
        ("Appointment Type", appointment.appointment_type or "N/A"),
        ("Appointment Date", f"{appointment.book_date} at {appointment.book_time}"),
        ("Patient Name", patient.name),
        ("Gender", patient.gender),
        ("Age", patient.age),
        ("Contact No.", patient.contact),
        
        ("Booking Date", appointment.curr_date.strftime("%d-%m-%Y %I:%M %p")),
        
    ]

    for label, value in fields:
        p.drawString(60, y, f"{label}:")
        p.drawString(200, y, str(value))
        y -= 18

    # ---------- NOTES ----------
    y -= 10
    p.setFont("Helvetica", 9)
    notes = [
        "* Reach hospital at least 30 minutes before scheduled time.",
        "* Carry valid ID proof and medical history if available.",
        "* Show this slip at reception. Appointment ID is required.",
        "* For online appointments, login to the portal for video consultation.",
    ]
    for note in notes:
        p.drawString(60, y, note)
        y -= 12

    # ---------- FINALIZE ----------
    p.showPage()
    p.save()
    buffer.seek(0)
    response.write(buffer.read())
    return response

def doctor_pat_show(request):

    if 'user_id' in request.session:
        a = request.session.get('user_id') 
        if not a:  
            return redirect('login')

        doc = get_object_or_404(Doctor, loginid=a)
        pat_show = Appointment.objects.filter(doc_id=doc)
        return render(request, 'pat_app_doc.html', {'pat_show': pat_show})
    else:
        return redirect('login')
# def presc_add(request, id):
#     appointment = get_object_or_404(Appointment, id=id) 

#     if request.method == 'POST':
#         form = Prescription(request.POST, instance=appointment) 
#         if form.is_valid():
#             form.save()  
#             return redirect('doc_mod')  

#     else:
#         form = Prescription(instance=appointment)  

#     return render(request, 'presc_add.html', {'form': form})
from django.shortcuts import render, get_object_or_404, redirect
from django.forms import formset_factory
from .models import Appointment, Prescription
from .forms import PrescriptionForm

def presc_add(request, id):
    if 'user_id' in request.session:
        appointment = get_object_or_404(Appointment, id=id)
        PrescriptionFormSet = formset_factory(PrescriptionForm, extra=1)
    
        if request.method == 'POST':
            formset = PrescriptionFormSet(request.POST)
            if formset.is_valid():
                for form in formset:
                    if form.cleaned_data.get("medicine_name"):  # Only save filled forms
                        prescription = form.save(commit=False)
                        prescription.appointment = appointment
                        # Assuming time_of_day is a multiple choice field returning list
                        time_of_day = form.cleaned_data.get("time_of_day")
                        if time_of_day:
                            prescription.time_of_day = ",".join(time_of_day)
                        prescription.save()
    
                return redirect('doc_mod')
    
        else:
            formset = PrescriptionFormSet()
    
        return render(request, 'presc_add.html', {'formset': formset})
    else:
        return redirect('login')

def pat_presc_show(request):
    user_id = request.session.get('user_id')
    patient = get_object_or_404(Patient, loginid=user_id)
    appointments = Appointment.objects.filter(pat_id=patient)
    
    # ✅ Fetch related prescriptions
    prescriptions = Prescription.objects.filter(appointment__in=appointments).order_by("start_date")

    return render(request, 'pat_presc_show.html', {'appointments': appointments, 'prescriptions': prescriptions})

# def doc_presc_show(request):
#     user_id = request.session.get('user_id')
#     doctor = get_object_or_404(Doctor, loginid=user_id)
#     appointments = Appointment.objects.filter(doc_id=doctor, pres__isnull=False)

#     return render(request, 'doc_presc_show.html', {'appointments': appointments})
 # ✅ Ensure it's imported

def doc_presc_show(request):
    if 'user_id' in request.session:
        user_id = request.session.get('user_id')
        doctor = get_object_or_404(Doctor, loginid=user_id)
        appointments = Appointment.objects.filter(doc_id=doctor)

        # ✅ Fetch all prescriptions related to the retrieved appointments
        prescriptions = Prescription.objects.filter(appointment__in=appointments).order_by("appointment__book_date")

        return render(request, 'doc_presc_show.html', {'appointments': appointments, 'prescriptions': prescriptions})
    else:
        return redirect('login')

def edit_presc(request, id):
    if 'user_id' in request.session:
        prescription = get_object_or_404(Prescription, id=id)  

        if request.method == 'POST':
            form = PrescriptionForm(request.POST, instance=prescription)  
            if form.is_valid():
                form.save()
                return redirect('doc_presc_show')  
        else:
            form = PrescriptionForm(instance=prescription)

        return render(request, 'edit_presc.html', {'form': form, 'patient': prescription.appointment.pat_id})
    else:
        return redirect('login')


def delete_presc(request, id):
    if 'user_id' in request.session:
        prescription = get_object_or_404(Prescription, id=id)  # ✅ Fetch correct prescription instance

        if request.method == 'POST':
            prescription.delete()  # ✅ Properly delete the prescription record
            return redirect('doc_presc_show')

        return render(request, 'delete_presc.html', {'prescription': prescription})
    else:
        return redirect('login')



def web_con(request,id):
    appointment = get_object_or_404(Appointment, id=id)
    return render(request,'WEB_UIKITS.html',{'appointment': appointment})

def save_appointment_url(request,id):
    if request.method == 'POST':
        data = json.loads(request.body)
        url = data.get('url')
        if url:
            appointment = get_object_or_404(Appointment, id=id)
            
            appointment.url = url
            
            appointment.save()

            return JsonResponse({'success': True, 'message': 'URL saved successfully'})

        return JsonResponse({'success': False, 'message': 'No URL provided'}, status=400)

    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)

def lab_reg(request):
    if 'user_id' in request.session:
        a=request.session.get('user_id')
        a1=get_object_or_404(Hosp,loginid=a)

        if request.method=='POST':
            form=Labuser(request.POST)
            form1=Log(request.POST)
            if form.is_valid() & form1.is_valid():
                f=form1.save(commit=False)
                f.usertype="lab"
                f.status=1
                f.save()

                f1=form.save(commit=False)
                f1.loginid=f
                f1.hosp_id=a1

                f1.save()
                return redirect('/')
        else:
                form=Labuser()
                form1=Log()

        return render(request,'lab_reg.html',{'form':form,'form1':form1})
    else:
        return redirect('login')
def lab_mod(request):
    if 'user_id' in request.session:
        return render(request,'lab_main2.html')
    else:
        return redirect('login')





def lab_profile_edit(request):
    if 'user_id' in request.session:
        user_id = request.session.get('user_id')
        login_data = get_object_or_404(Login, id=user_id)
        lab_data = get_object_or_404(Lab, loginid=login_data)  

        return render(request, 'lab_profile_edit.html', {'lab_data': lab_data})
    else:
        return redirect('login')

   
def lab_doc_show(request,id):
    if 'user_id' in request.session:
        user_id = request.session.get('user_id')
        lab = get_object_or_404(Doctor, loginid=user_id)
        app_id = get_object_or_404(Appointment, id=id)
        a = Lab.objects.filter(hosp_id=lab.hosp_name)

        return render(request, 'labs_show_doc.html', {'a': a,'app_id':app_id})
    else:
        return redirect('login')
# def lab_test_doc(request, id, lab_id): 
#     f = get_object_or_404(Appointment, id=id)
#     f1 = get_object_or_404(Lab, id=lab_id)
    
#     if request.method == 'POST':  
#         form = Labtestform(request.POST)
#         if form.is_valid():
#             a = form.save(commit=False)
#             a.app_id = f
#             a.lab_id = f1
#             a.status = 0  # Initial status (Payment Pending)
#             a.save()
#             return redirect('doc_mod')
#     else:
#         form = Labtestform()            
    
#     return render(request, 'lab_test_doc.html', {'form': form})
def lab_test_doc(request, id, lab_id): 
    if 'user_id' in request.session:
        f = get_object_or_404(Appointment, id=id)
        f1 = get_object_or_404(Lab, id=lab_id)

        if request.method == 'POST':  
            form = Labtestform(request.POST)
            if form.is_valid():
                a = form.save(commit=False)
                a.app_id = f
                a.lab_id = f1
                a.status = 0  # Payment Pending

                selected_tests = form.cleaned_data['selected_tests']

                a.test_details = ', '.join([test[0] for test in Labtestform.TEST_CHOICES if test[0] in selected_tests])
                a.test_prices = {test[0]: test[1] for test in Labtestform.TEST_CHOICES if test[0] in selected_tests}

                # ✅ Calculate and assign total_price
                total = 0
                for test in selected_tests:
                    for name, label in Labtestform.TEST_CHOICES:
                        if test == name:
                            total += int(label.split('₹')[1])
                a.total_price = total

                a.save()
                return redirect('doc_mod')
        else:
            form = Labtestform()            

        return render(request, 'lab_test_doc.html', {'form': form})
    else:
        return redirect('login')

def patient_lab_tests(request):
    if 'user_id' in request.session:
        user_id = request.session.get('user_id')  
        patient_appointments = Appointment.objects.filter(pat_id__loginid=user_id)  
        lab_tests = Labtest.objects.filter(app_id__in=patient_appointments)

        # ✅ Calculate total price for each test
        for test in lab_tests:
            test.calculated_price = test.total_price  # ✅ Ensure each test carries its total price

        return render(request, 'patient_lab_tests.html', {'lab_tests': lab_tests})
    else:
        return redirect('login')    
def lab_show_doc_request(request):
    if 'user_id' in request.session:
        user_id = request.session.get("user_id")  
        if not user_id:  
            return redirect("login")
    
        lab = get_object_or_404(Lab, loginid=user_id)
    
        # ✅ Fetch all lab tests, both paid and unpaid
        lab_show = Labtest.objects.filter(lab_id=lab)  # Removed status=1 filter
    
        return render(request, "lab_show_doc_request.html", {"lab_show": lab_show})
    else:
        return redirect('login')

def update_lab_status(request, lab_test_id):

    if request.method == "POST":
        lab_test = Labtest.objects.get(id=lab_test_id)
        lab_test.status = 1  # Update status to Paid
        lab_test.save()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False})



def lab_file_upload(request, id):
    if 'user_id' in request.session:
        f = get_object_or_404(Labtest, id=id)
        if request.method == 'POST': 

            rep_text = request.POST.get('report_given') 

            if rep_text:
                f.report_given = rep_text  
            f.save()
            return redirect('lab_mod')  
        return render(request, 'lab_file_upload.html', {'labtest': f})
    else:
        return redirect('login')

def lab_report_show_doc(request):
    if 'user_id' in request.session:
        a = request.session.get('user_id') 
        if not a:  
            return redirect('login')
        doc = get_object_or_404(Doctor, loginid=a)
        lab_show = Labtest.objects.filter(app_id__doc_id=doc)  
        return render(request, 'lab_report_show_doc.html', {'lab_show': lab_show})
    else:
        return redirect('login')

def lab_report_show_pat(request):
    if 'user_id' in request.session:
        a = request.session.get('user_id') 
        if not a:  
            return redirect('login')
        pat = get_object_or_404(Patient, loginid=a)
        lab_show = Labtest.objects.filter(app_id__pat_id=pat)  
        return render(request, 'lab_report_show_pat.html', {'lab_show': lab_show})
    else:
        return redirect('login')




def generate_lab_report(request, labtest_id):
    labtest = Labtest.objects.get(id=labtest_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Lab_Report_{labtest.id}.pdf"'

    p = canvas.Canvas(response)
    p.setFont("Helvetica-Bold", 18)
    p.drawString(200, 800, "LAB TEST REPORT")

    # Section: Basic Information
    p.setFont("Helvetica", 14)
    p.drawString(100, 770, f"Lab Report ID: {labtest.id}")
    p.drawString(100, 750, f"Patient Name: {labtest.app_id.pat_id.name}")
    p.drawString(100, 730, f"Doctor: {labtest.app_id.doc_id.name}")
    p.drawString(100, 710, f"Hospital: {labtest.app_id.hosp_id.name}")

    # Section: Test Details
    p.setFont("Helvetica-Bold", 14)
    p.drawString(100, 690, "Test Details:")
    p.setFont("Helvetica", 12)
    p.drawString(120, 670, f"{labtest.test_details}")

    # Section: Lab Report Findings
    p.setFont("Helvetica-Bold", 14)
    p.drawString(100, 650, "Result Details:")
    p.setFont("Helvetica", 12)
    p.drawString(120, 630, f"{labtest.report_given}")  # ✅ Now fetching `report_text` for lab findings

    # Section: Date & Footer
    p.setFont("Helvetica", 12)
    p.drawString(100, 600, f"Date Generated: {labtest.curr_date.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Footer Message
    p.setFont("Helvetica-Oblique", 12)
    p.drawString(200, 570, "Thank you for choosing our laboratory services.")

    # Finalize PDF
    p.showPage()
    p.save()

    return response



def lab_edit_del(request):
    if 'user_id' in request.session:
        user_id = request.session.get('user_id')
        if not user_id:  
            return redirect('login')
        lab = get_object_or_404(Lab, loginid=user_id) 
        lab_tests = Labtest.objects.filter(lab_id=lab)  
        return render(request, 'lab_edit_del.html', {'lab_tests': lab_tests})
    else:
        return redirect('login')


def edit_report(request, id):
    if 'user_id' in request.session:
        labtest = get_object_or_404(Labtest, id=id)
        if request.method == 'POST':
            labtest.report_given = request.POST.get('report_given')
            labtest.save()
            return redirect('lab_edit_del')  
        return render(request, 'edit_report.html', {'labtest': labtest})  
    else:
        return redirect('login')

def delete_report(request, id):

    labtest = get_object_or_404(Labtest, id=id)
    labtest.delete()
    return redirect('lab_edit_del')  

def reg_inc(request):
    
    if request.method == 'POST':
        form = Incuser(request.POST)
        form1 = Log(request.POST)
        if form.is_valid() and form1.is_valid():
            f = form1.save(commit=False)
            f.usertype = "insurance"
            f.status = 1
            f.save()
            f1 = form.save(commit=False)
            f1.loginid = f
            f1.save()  # ✅ No need to manually set inc_id; it's auto-generated
            return redirect('/')
    else:
        form = Incuser()
        form1 = Log()      
    return render(request, 'reg_inc.html', {'form': form, 'form1': form1})
  

def inc_mod(request):
    if 'user_id' in request.session:
        return render(request,'inc_main2.html')
    else:
        return redirect('login')

def inc_pro_edit(request):
    if 'user_id' in request.session:
        a=request.session.get('user_id')
        print(a)
        a1=get_object_or_404(Login,id=a)
        logindata=get_object_or_404(Login,id=a1.id)
        inc_data=get_object_or_404(Insurance,loginid=a)
        if request.method=='POST':
            form=Incuser(request.POST,request.FILES,instance=inc_data)
            form1=EmailUpdate(request.POST,instance=logindata)
            if form.is_valid() and form1.is_valid():
                form.save()
                form1.save()
                return redirect('inc_mod')
        else:
                form=Incuser(instance=inc_data)
                form1=EmailUpdate(instance=logindata)
        return render(request,'inc_pro_edit.html',{'form1':form,'form2':form1})
    else:
        return redirect('login')


def ins_scheme(request):
    if 'user_id' in request.session:
        if request.method == "POST":
            category = request.POST.get("category")
            scheme_name = request.POST.get("scheme_name")
            details = request.POST.get("details")
            type = request.POST.get("payment_type")
            amount = "0" if type == "cashless" else request.POST.get("amount")
            ins_taken = Ins_taken(category=category, scheme_name=scheme_name , details=details, amount=amount, type=type)
            ins_taken.save()  
            return redirect("inc_mod")  
        return render(request, "ins_scheme.html")
    else:
        return redirect('login')

def ins_pat_show(request):
    if 'user_id' in request.session:
        ins=Hosp.objects.all()
        return render(request,'ins_pat_show.html',{'ins':ins})
    else:
        return redirect('login')


def ins_pat_hosp_show(request, id):
    if 'user_id' in request.session:
        hospital = get_object_or_404(Hosp, id=id)
        insurance_schemes = Ins_taken.objects.all()

        return render(request, "ins_pat_hosp_show.html", {"hospital": hospital, "insurance_schemes": insurance_schemes})
    else:
        return redirect('login')



def ins_details_pat(request, id, hosp_id):
    if 'user_id' in request.session:
        patid = request.session.get('user_id')
        ins_scheme = get_object_or_404(Ins_taken, id=id)  
        hosp = get_object_or_404(Hosp, id=hosp_id)  
        pat=get_object_or_404(Patient,loginid=patid)
        # ✅ Fetch doctors of the selected hospital
        doctors = Doctor.objects.filter(hosp_name=hosp)

        if request.method == "POST":

            disease_name = request.POST.get("disease_name")
            doc_id = request.POST.get("doctor_name")  
            ins_num = request.POST.get("ins_number")
            details = request.POST.get("details_disease")

            doctor = get_object_or_404(Doctor, id=doc_id)

            ins_pat = Ins_pat(
                hosp_id=hosp,
                pat_id=pat,
                disease_name=disease_name,
                doc_name=doctor.name,  
                ins_num=ins_num,
                details=details
            )
            ins_pat.save()

            return redirect("pat_mod")

        return render(request, "ins_details_pat.html", {"ins_scheme": ins_scheme, "hosp": hosp, "doctors": doctors})
    else:
        return redirect('login')


def hosp_pat_ins_req(request):
    if 'user_id' in request.session:
        if not request.session.get('user_id'):  
            return redirect('login')
        user_id = request.session.get('user_id') 
        hosp = get_object_or_404(Hosp, loginid_id=user_id) 
        patient_requests = Ins_pat.objects.filter(hosp_id=hosp)

        return render(request, 'hosp_pat_ins_req.html', {"patient_requests": patient_requests, "hospital": hosp})
    else:
        return redirect('login')


def verify_ins(request, id):
    if 'user_id' in request.session:
        insurance_request = get_object_or_404(Ins_pat, id=id)

        if request.method == "POST":
            insurance_request.status = 1  
            insurance_request.file = request.FILES.get("file")  # ✅ Capture uploaded file
            insurance_request.save()
            return redirect("hosp_pat_ins_req")

        return render(request, "verify_ins.html", {"insurance_request": insurance_request})
    else:
        return redirect('login')

def verified_list(request):
    if 'user_id' in request.session:
        verifyed = Ins_pat.objects.filter(status=1)
        return render(request, "verified_list.html", {"verifyed": verifyed})
    else:
        return redirect('login')


def ins_accept(request, id, action):
    insurance_request = get_object_or_404(Ins_pat, id=id)

    if action == "accept":
        insurance_request.sa = 1
    elif action == "reject":
        insurance_request.sa = 2 
    
    insurance_request.save()
    return redirect("verified_list") 




def pat_ins_req_show(request):
    if 'user_id' in request.session:
        a = request.session.get('user_id') 
        pat = get_object_or_404(Patient, loginid=a)
        insurance_requests = Ins_pat.objects.filter(pat_id=pat)
        return render(request, 'pat_ins_req_show.html', {"patient": pat, "insurance_requests": insurance_requests})
    else:
        return redirect('login')


def pat_ins_track(request, id):
    if 'user_id' in request.session:
        if not request.session.get('user_id'):  
            return redirect("login")

        user_id = request.session.get('user_id') 
        patient = get_object_or_404(Patient, loginid_id=user_id) 
        insurance_request = get_object_or_404(Ins_pat, id=id, pat_id=patient)

        return render(request, "pat_ins_track.html", {"patient": patient, "insurance_request": insurance_request})
    else:
        return redirect('login')


def hosp_pat_ins_status(request):
    if 'user_id' in request.session:
        if not request.session.get('user_id'):  
            return redirect("login") 
        user_id = request.session.get('user_id') 
        hospital = get_object_or_404(Hosp, loginid_id=user_id)  
        patient_requests = Ins_pat.objects.filter(hosp_id=hospital)
        return render(request, "hosp_pat_ins_status.html", {"hospital": hospital, "patient_requests": patient_requests})
    else:
        return redirect('login')

def hosp_pat_req_track(request, id):
    if 'user_id' in request.session:
        if not request.session.get('user_id'):  
            return redirect("login") 
        insurance_request = get_object_or_404(Ins_pat, id=id)
        return render(request, "hosp_pat_req_track.html", {"insurance_request": insurance_request})
    else:
        return redirect('login')


def claim_amt_tr(request, id):
    if 'user_id' in request.session:
        insurance_request = get_object_or_404(Ins_pat, id=id)
        if request.method == "POST":
            amount = request.POST.get("amt")  
            insurance_request.amt = amount
            insurance_request.ins_amt_status = 1  
            insurance_request.save()
            return redirect("verified_list")
        return render(request, "claim_amt_tr.html", {"insurance_request": insurance_request})
    else:
        return redirect('login')




def all_pat_prnumber(request):
    if 'user_id' in request.session:
        pr_number = request.GET.get("pr_number")
        patient = None
        appointments = None
        prescriptions = None
        lab_tests = None  # ✅ Initialize variable to prevent errors
        insurance_details = None  # ✅ Initialize variable to prevent errors
        error_message = None  

        if pr_number:
            try:
                patient = get_object_or_404(Patient, pr_number=pr_number)
                appointments = Appointment.objects.filter(pat_id=patient).prefetch_related('prescriptions')

                # ✅ Fetch prescriptions for all appointments
                prescriptions = Prescription.objects.filter(appointment__in=appointments).order_by("start_date")

                # ✅ Fetch lab tests and insurance details safely
                lab_tests = Labtest.objects.filter(app_id__pat_id=patient)
                insurance_details = Ins_pat.objects.filter(pat_id=patient)
            except Patient.DoesNotExist:
                error_message = f"No patient found with registration number '{pr_number}'"

        return render(request, "all_pat_prnumber.html", {
            "patient": patient,
            "appointments": appointments,
            "prescriptions": prescriptions,
            "lab_tests": lab_tests, 
            "insurance_details": insurance_details,
            "error_message": error_message  
        })
    else:
        return redirect('login')
def all_pat_prnumber_hosp(request):
    if 'user_id' in request.session:
        pr_number = request.GET.get("pr_number")
        patient = None
        appointments = None
        lab_tests = None
        insurance_details = None
        error_message = None  
    
        if pr_number:
            try:
                patient = get_object_or_404(Patient, pr_number=pr_number)
                appointments = Appointment.objects.filter(pat_id=patient)
                lab_tests = Labtest.objects.filter(app_id__pat_id=patient)
                insurance_details = Ins_pat.objects.filter(pat_id=patient)
                
            except:
                error_message = f"No patient found with registration number '{pr_number}'"
    
        return render(request, "all_pat_prnumber_hosp.html", {
            "patient": patient,
            "appointments": appointments,
            "lab_tests": lab_tests,
            "insurance_details": insurance_details,
            "error_message": error_message  
        })
    else:
        return redirect('login')


def dashboard_analytics(request):
    # Number of registered patients
    total_patients = Patient.objects.count()

    # Number of doctors in the hospital
    total_doctors = Doctor.objects.count()

    # Insurance requests
    insurance_requested = Ins_pat.objects.count()

    # Approved insurance claims
    insurance_approved = Ins_pat.objects.filter(status=1).count()
    print(total_patients)
    return render(request, "dashboard.html", {
        "total_patients": total_patients,
        "total_doctors": total_doctors,
        "insurance_requested": insurance_requested,
        "insurance_approved": insurance_approved
    })




def hosp_pat_appointment(request):
    if 'user_id' in request.session:
        user_id = request.session.get('user_id') 
        hosp = get_object_or_404(Hosp, loginid=user_id)  
        pat_show = Appointment.objects.filter(hosp_id=hosp) 

        return render(request, 'hosp_pat_appointment.html', {'pat_show': pat_show, 'hosp': hosp})
    else:
        return redirect('login')
def hosp_docs_show(request):
    if 'user_id' in request.session:
        user_id = request.session.get('user_id')  
        hosp = get_object_or_404(Hosp, loginid=user_id)  
        doc_show = Doctor.objects.filter(hosp_name=hosp)  

        return render(request, 'hosp_docs_show.html', {'doc_show': doc_show, 'hosp': hosp})
    else:
        return redirect('login')
def update_doctor_fee(request, doctor_id):
    if 'user_id' in request.session:
        doctor = get_object_or_404(Doctor, id=doctor_id)

        if request.method == 'POST':
            con_fee = request.POST.get('con_fee')
            doctor.con_fee = con_fee
            doctor.save()
            return redirect('hosp_docs_show')  # Redirect back to the page after saving

        return render(request, 'hosp_docs_show.html')
    else:
        return redirect('login')


def ins_show_admin(request):
    if 'user_id' in request.session:
        ins_show=Insurance.objects.all()
        return render(request,'ins_show_admin.html',{'ins_show':ins_show})
    else:
        return redirect('login')
   
def ins_pat_show_admin(request):
    if 'user_id' in request.session:
        ins_show=Ins_pat.objects.all()
        return render(request,'ins_pat_show_admin.html',{'ins_show':ins_show})
    else:
        return redirect('login')
   
def labs_show_admin(request):
    if 'user_id' in request.session:
        lab_show=Lab.objects.all()
        return render(request,'labs_show_admin.html',{'lab_show':lab_show})
    else:
        return redirect('login')   

def logout(request):
    request.session.flush()
    return redirect('index')
   



def complaint_view(request):
    user_id = request.session.get('user_id')  
    patient = Patient.objects.get(loginid=user_id) 

    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.patient = patient  
            complaint.save()
            return redirect('pat_mod')  

    else:
        form = ComplaintForm()

    return render(request, 'complaint_form.html', {'form': form, 'patient': patient})



def admin_complaint_list(request):
    complaints = Complaint.objects.all().order_by("-submitted_at")  # ✅ Fetch complaints in descending order
    return render(request, "admin_complaint_list.html", {"complaints": complaints})

def admin_reply(request, id):
    complaint = get_object_or_404(Complaint, id=id)

    if request.method == "POST":
        form = ResponseForm(request.POST, instance=complaint)
        if form.is_valid():
            complaint = form.save(commit=False)
            
            complaint.save()
            return redirect("admin_complaint_list")  # ✅ Redirect back to complaint list

    else:
        form = ResponseForm(instance=complaint)

    return render(request, "admin_reply.html", {"form": form, "complaint": complaint})



def patient_complaint_list(request):
    if 'user_id' in request.session:
        user_id = request.session.get('user_id')  # ✅ Get logged-in user ID
        patient = get_object_or_404(Patient, loginid=user_id)  # ✅ Retrieve patient object
        complaints = Complaint.objects.filter(patient=patient).order_by("-submitted_at")  # ✅ Fetch patient's complaints

        return render(request, "patient_complaints.html", {"complaints": complaints, "patient": patient})
    else:
        return redirect('login') 


def donate_organ(request):
    if 'user_id' in request.session:
        if request.method == 'POST':
            form = DonationForm(request.POST, request.FILES) 
            if form.is_valid():
                form.save()
                return redirect('hosp_mod') 

        else:
            form = DonationForm()

        return render(request, 'donation_form.html', {'form': form})
    else:
        return redirect('login')



def recipient_form(request):
    if 'user_id' in request.session:
        if request.method == 'POST':
            form = RecipientForm(request.POST)
            if form.is_valid():
                recipient = form.save()

                matched_donors = Donation.objects.filter(
                    blood_group=recipient.blood_group,
                    organ_name__iexact=recipient.organ_needed  
                )

                for donor in matched_donors:
                    OrganMatch.objects.create(recipient=recipient, donor=donor)


                return redirect('matches', blood_group=recipient.blood_group, organ_needed=recipient.organ_needed)

        else:
            form = RecipientForm()

        return render(request, 'recipient_form.html', {'form': form})
    else:
        return redirect('login')

def matches(request, blood_group, organ_needed):
    if 'user_id' in request.session:
        matched_donors = Donation.objects.filter(
            blood_group=blood_group,
            organ_name__iexact=organ_needed
        )

        print("Matched Donors Found:", matched_donors)  

        return render(request, "matches.html", {
            "blood_group": blood_group,
            "organ_needed": organ_needed,
            "matched_donors": matched_donors
        })
    else:
        return redirect('login')

def update_lab_payment(request, test_id):
    if 'user_id' in request.session:
        lab_test = get_object_or_404(Labtest, id=test_id)
    
        
        print("DEBUG - Labtest Total Price:", lab_test.total_price)
    
        if request.method == "POST":
            lab_test.card_name = request.POST.get("card_name")
            lab_test.card_number = request.POST.get("card_number")
            lab_test.exp_date = request.POST.get("exp")
            lab_test.cvv = request.POST.get("cvv")
            lab_test.status = 1  
            lab_test.save()
            
            return redirect("patient_lab_tests")  
    
        return render(request, "payment_page.html", {"lab_test": lab_test, "total_price": lab_test.total_price})
    else:
        return redirect('login')



from django.shortcuts import render
from .forms import xrayform
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os

def xray(request):
    predicted_disease = None

    if request.method == 'POST':
        form = xrayform(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['Image']

            # Save the uploaded file properly
            fs = FileSystemStorage()
            filename = fs.save(image.name, image)

            # Get the full path to the saved file
            full_image_path = fs.path(filename)

            # Call your prediction function with full path
            predicted_disease = predict_disease(full_image_path)

    else:
        form = xrayform()
    
    return render(request, 'xray.html', {
        'form': form,
        'predicted_disease': predicted_disease
    })


def ask(request):
    return render(request, 'chatbot.html')
import requests
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings

# For parsing form data
from django.views.decorators.http import require_POST
import re

def format_ai_response(ai_answer):
    # Replace bold (**text**) with <strong>text</strong>
    ai_answer = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', ai_answer)
    
    # Replace numbered list 1. 2. with <ol><li>...</li></ol> (basic approximation)
    ai_answer = re.sub(r'(\n|^)\d+\.\s+(.*)', r'<li>\2</li>', ai_answer)

    # Replace hyphen lists - with <ul><li>...</li></ul> (basic)
    ai_answer = re.sub(r'(\n|^)-\s+(.*)', r'<li>\2</li>', ai_answer)

    # Replace double newlines with paragraph breaks
    ai_answer = ai_answer.replace('\n\n', '</p><p>')
    ai_answer = '<p>' + ai_answer + '</p>'
    
    return ai_answer

# Optional: Add logging for production
import logging
logger = logging.getLogger(__name__)

# You may store your API key securely in settings.py or environment variables
NEMOTRON_API_KEY = settings.NEMOTRON_API_KEY  # Read from Django settings for security

@csrf_exempt
@require_POST
def ask_health(request):
    try:
        question = request.POST.get('question', '').strip()

        if not question:
            return JsonResponse({'error': 'Please provide a health-related question.'}, status=400)

        # Build request for NemoTron API
        api_url = "https://integrate.api.nvidia.com/v1/chat/completions"
        headers = {
            'Authorization': f'Bearer {NEMOTRON_API_KEY}',
            'Content-Type': 'application/json'
        }

        payload = {
            "model":"nvidia/llama-3.1-nemotron-70b-instruct",  # Replace with the actual model you have access to
            "messages": [
    {
        "role": "system",
        "content": (
            "You are a certified AI health assistant. "
            "Only answer health-related questions such as symptoms, diseases, remedies, medication, precautions, or general health advice. "
            "If the user asks anything unrelated to health (e.g. politics, sports, entertainment, finance, programming, etc), politely reply: "
            "'I'm here to assist you with health-related information. Please ask me a health-related question.' "
            "Never answer unrelated questions."
        )
    },
    {"role": "user", "content": question}
],

            "temperature": 0.5,
            "max_tokens": 800,
            "top_p": 1.0
        }

        response = requests.post(api_url, headers=headers, json=payload)

        if response.status_code != 200:
            logger.error(f"NemoTron API Error: {response.status_code} - {response.text}")
            return JsonResponse({'error': 'AI service is temporarily unavailable.'}, status=500)

        data = response.json()

        # Extract AI response (adapt if structure differs)
        ai_answer = data['choices'][0]['message']['content'].strip()
        formatted_answer = format_ai_response(ai_answer)
        return JsonResponse({'answer': formatted_answer})

    except Exception as e:
        logger.exception("Error during health chatbot processing")
        return JsonResponse({'error': 'An unexpected error occurred. Please try again later.'}, status=500)


def transfer_patient(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    doctors = Doctor.objects.exclude(id=appointment.doc_id.id)  # Exclude current doctor

    if request.method == "POST":
        transfer_doc_id = request.POST.get("transfer_doc_id")
        transfer_doc = get_object_or_404(Doctor, id=transfer_doc_id)

        TransferAppointment.objects.create(
            pat_id=appointment.pat_id,
            doc_id=appointment.doc_id,
            transfer_doc_id=transfer_doc
        )

        return redirect("doctor_pat_show")  # Redirect back to appointments page

    return render(request, "transfer_patient.html", {"doctors": doctors, "appointment": appointment})




def transferred_patients(request):
    if "user_id" in request.session:
        doctor_id = request.session.get("user_id")
        
        try:
            doctor = Doctor.objects.get(loginid=doctor_id)
        except Doctor.DoesNotExist:
            return redirect("login")  # Redirect if doctor does not exist

        # Fetch patients transferred to the logged-in doctor
        transferred_patients = TransferAppointment.objects.filter(transfer_doc_id=doctor)

        return render(request, "transferred_patients.html", {
            "doctor": doctor,
            "transferred_patients": transferred_patients
        })

    return redirect("login")  # Redirect if session is missing
