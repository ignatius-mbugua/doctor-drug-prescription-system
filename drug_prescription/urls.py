"""drug_prescription URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from users import views as user_views
from prescription import views as pre_views

urlpatterns = [
    # administration
    path('admin/', admin.site.urls),

    # index
    path('', pre_views.index, name='index'),

    # authentication
    path('register/', user_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),

    # patient crud urls
    path('patients/', pre_views.patient_list, name='patients-list'),
    path('patients/create/', pre_views.patient_create, name='patients-create'),
    path('patients/<int:id>/update', pre_views.patient_update, name='patients-update'),
    path('patients/<int:id>/delete', pre_views.patient_delete, name='patients-delete'),

    #prescribing
    path('prescriptions/', pre_views.prescribe_list, name='prescribe-list'),
    path('prescriptions/create/', pre_views.prescribe_create, name='prescribe-create'),
    path('prescriptions/<int:id>/medicine', pre_views.prescribe_medicine, name='prescribe-medicine'),
    path('prescriptions/<int:id>/delete', pre_views.prescribe_delete, name='prescribe-delete'),
    path('prescriptions/<int:id>/update', pre_views.prescribe_update, name='prescribe-update'),

    # reports
    path('patients/report/', pre_views.patient_reports, name='patients-reports'),
    path('patients/report-gender', pre_views.print_gender_chart, name='print-gender-chart'),
    path('patients/report-malaria-medicine', pre_views.print_malaria_medicine_chart, name='print-malaria-medicine-chart'),
    path('patients/report-tuberculosis-medicine', pre_views.print_tuberculosis_medicine_chart, name='print-tuberculosis-medicine-chart'),

    # report data
    path('gender-data/', pre_views.gender_chart_data, name='gender-data'),
    path('malaria-medicine-data/', pre_views.malaria_medicine_chart_data, name='malaria-medicine-data'),
    path('tuberculosis-medicine-data/', pre_views.tuberculosis_medicine_chart_data, name='tuberculosis-medicine-data'),
]
