from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Patient, PatientDetail
from .forms import PatientForm, PatientUpdateForm, PatientDetailForm, PatientDetailUpdateForm
from django.contrib import messages
import pickle
from django.contrib.staticfiles.templatetags.staticfiles import static
import os
from django.http import JsonResponse


#index page
def index(request):
    return render(request, 'prescription/index.html')


# list of all prescribed patients
@login_required
def prescribe_list(request):
    patients_records = PatientDetail.objects.all().order_by('-created_at')
    context = {'patients_records': patients_records}
    return render(request, 'prescription/prescribe-list.html', context)

# form to create patient detail
@login_required
def prescribe_create(request):
    if request.method == 'POST':
        patient_detail_form = PatientDetailForm(data=request.POST)
        if patient_detail_form.is_valid():
            last_record_object = patient_detail_form.save()
            last_record_object_id = last_record_object.id
            return redirect('prescribe-medicine', last_record_object_id)
        else:
            messages.error(request, "Please fill all details correctly")
    else:
        patient_detail_form = PatientDetailForm()
    return render(request, 'prescription/prescribe-create.html', {'patient_detail_form': patient_detail_form})

# form to update patient detail
@login_required
def prescribe_update(request, id):
    patient = PatientDetail.objects.get(id=id)
    if request.method == 'POST':
        patient_detail_update_form = PatientDetailUpdateForm(instance=patient, data=request.POST)
        if patient_detail_update_form.is_valid():
            patient_detail_update_form.save()
            return redirect('prescribe-list')
        else:
            messages.error(request, "Please fill all details correctly")
    else:
        patient_detail_update_form = PatientDetailUpdateForm(instance=patient)
    return render(request, 'prescription/prescribe-update.html', {'patient_detail_update_form': patient_detail_update_form})

# predict patients medicine
@login_required
def prescribe_medicine(request, id):
    pt_record = PatientDetail.objects.get(id=id)

    # TODO:predict medicine and show image of how it was arrived at
    #data preprocessing
    age = pt_record.patient.age
    if pt_record.patient.gender == 'MALE':
        gender = 1
    elif pt_record.patient.gender == 'FEMALE':
        gender = 0

    if pt_record.breast_feeding == 'Y':
        breast_feeding = 1
    elif pt_record.breast_feeding == 'N':
        breast_feeding = 0

    if pt_record.alcoholic == 'Y':
        alcoholic = 1
    elif pt_record.alcoholic == 'N':
        alcoholic = 0

    if pt_record.pregnant == 'Y':
        pregnancy = 1
    elif pt_record.pregnant == 'N':
        pregnancy = 0

    if pt_record.liver_disease == 'Y':
        liver_disease = 1
    elif pt_record.liver_disease == 'N':
        liver_disease = 0

    if pt_record.eye_disease == 'Y':
        eye_disease = 1
    elif pt_record.eye_disease == 'N':
        eye_disease = 0

    if pt_record.kidney_disease == 'Y':
        kidney_disease = 1
    elif pt_record.kidney_disease == 'N':
        kidney_disease = 0

    if pt_record.diabetes == 'Y':
        diabetes = 1
    elif pt_record.diabetes == 'N':
        diabetes = 0

    weight = pt_record.weight_in_kg

    if pt_record.disease_identified == 'Malaria':
        # load model for malaria
        path_to_model = os.getcwd() + '/prescription/static/prescription/models/md_malaria_medicine'
        with open(path_to_model, 'rb') as f:
            model = pickle.load(f)

        # prediction
        prediction = model.predict([[age, gender, pregnancy, breast_feeding, alcoholic, liver_disease, eye_disease,
        kidney_disease, diabetes, weight]])
        if prediction == 1:
            medicine_identified = "Doxycycline"
        elif prediction == 2:
            medicine_identified = "Lariam"
        elif prediction == 3:
            medicine_identified = "Malarone"

    elif pt_record.disease_identified == 'Tuberculosis':
        # load model for tuberculosis
        path_to_model = os.getcwd() + '/prescription/static/prescription/models/md_tuberculosis_medicine'
        with open(path_to_model, 'rb') as f:
            model = pickle.load(f)

        # prediction
        prediction = model.predict([[age, gender, pregnancy, breast_feeding, alcoholic, liver_disease, eye_disease,
        kidney_disease, diabetes, weight]])
        if prediction == 1:
            medicine_identified = "Rifater"
        elif prediction == 2:
            medicine_identified = "Ethambutol"
        elif prediction == 3:
            medicine_identified = "Isoniazid"


    # save medicine identified
    pt_record.medicine = medicine_identified
    pt_record.save()

    context = {
        'medicine_identified': medicine_identified,
        'pt_record': pt_record
    }
    return render(request, 'prescription/prescribe-medicine.html', context)

# delete patient's prescription record
@login_required
def prescribe_delete(request, id):
    pt_record = PatientDetail.objects.get(id=id)
    pt_record.delete()

    return redirect('prescribe-list')


# list patient's record
@login_required
def patient_list(request):
    patients = Patient.objects.all().order_by('-created_at')
    total_patients = patients.count()
    female_patients = Patient.objects.filter(gender='FEMALE').count()
    male_patients = Patient.objects.filter(gender='MALE').count()
    context = {
        'patients': patients,
        'total_patients': total_patients,
        'female_patients': female_patients,
        'male_patients': male_patients
    }
    return render(request, 'prescription/patients.html', context)


# delete patient's record
@login_required
def patient_delete(request, id):
    pt = Patient.objects.get(id=id)
    pt.delete()

    return redirect('patients-list')

# create patient's record
@login_required
def patient_create(request):
    if request.method == 'POST':
        patient_form = PatientForm(data=request.POST)
        if patient_form.is_valid():
            patient_form.save()
            return redirect('patients-list')
        else:
            messages.error(request, "Please fill all details correctly")
    else:
        patient_form = PatientForm()
    return render(request, 'prescription/patients-create.html', {'patient_form': patient_form})


# update patient's record
@login_required
def patient_update(request, id):
    patient = Patient.objects.get(id=id)
    if request.method == 'POST':
        patient_update_form = PatientUpdateForm(instance=patient, data=request.POST)
        if patient_update_form.is_valid():
            patient_update_form.save()
            return redirect('patients-list')
        else:
            messages.error(request, "Please fill all details correctly")
    else:
        patient_update_form = PatientUpdateForm(instance=patient)
    return render(request, 'prescription/patients-update.html', {'patient_update_form': patient_update_form})


#patient reports
@login_required
def patient_reports(request):
    return render(request, 'prescription/patients-reports.html')


#gender chart data
@login_required
def gender_chart_data(request):
    female_patients = Patient.objects.filter(gender='FEMALE').count()
    male_patients = Patient.objects.filter(gender='MALE').count()
    gender_count = [female_patients, male_patients]

    data = {
        'gender_count': gender_count
    }
    return JsonResponse(data)

@login_required
def print_gender_chart(request):
    female_patients = Patient.objects.filter(gender='FEMALE').count()
    male_patients = Patient.objects.filter(gender='MALE').count()
    context = {
        'female_patients': female_patients,
        'male_patients': male_patients
    }
    return render(request, 'prescription/report-gender.html', context)


#tuberculosis chart data
@login_required
def malaria_medicine_chart_data(request):
    doxycycline_count = PatientDetail.objects.filter(medicine='Doxycycline').count()
    lariam_count = PatientDetail.objects.filter(medicine='Lariam').count()
    malarone_count = PatientDetail.objects.filter(medicine='Malarone').count()
    malaria_count = [doxycycline_count, lariam_count, malarone_count]

    data = {
        'malaria_count': malaria_count
    }
    return JsonResponse(data)


@login_required
def print_malaria_medicine_chart(request):
    doxycycline_count = PatientDetail.objects.filter(medicine='Doxycycline').count()
    lariam_count = PatientDetail.objects.filter(medicine='Lariam').count()
    malarone_count = PatientDetail.objects.filter(medicine='Malarone').count()
    context = {
        'doxycycline_count': doxycycline_count,
        'lariam_count': lariam_count,
        'malarone_count': malarone_count
    }
    return render(request, 'prescription/report-malaria-medicine.html', context)

#tuberculosis chart data
@login_required
def tuberculosis_medicine_chart_data(request):
    rifater_count = PatientDetail.objects.filter(medicine='Rifater').count()
    ethambutol_count = PatientDetail.objects.filter(medicine='Ethambutol').count()
    isoniazid_count = PatientDetail.objects.filter(medicine='Isoniazid').count()
    tuberculosis_count = [rifater_count, ethambutol_count, isoniazid_count]

    data = {
        'tuberculosis_count': tuberculosis_count
    }
    return JsonResponse(data)


@login_required
def print_tuberculosis_medicine_chart(request):
    rifater_count = PatientDetail.objects.filter(medicine='Rifater').count()
    ethambutol_count = PatientDetail.objects.filter(medicine='Ethambutol').count()
    isoniazid_count = PatientDetail.objects.filter(medicine='Isoniazid').count()
    context = {
        'rifater_count': rifater_count,
        'ethambutol_count': ethambutol_count,
        'isoniazid_count': isoniazid_count
    }
    return render(request, 'prescription/report-tuberculosis-medicine.html', context)
