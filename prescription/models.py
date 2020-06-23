from django.db import models
from django.urls import reverse
from django.utils import timezone


# Create your models here.

#select choices
GENDER_CHOICES = (
    ('MALE', 'male'),
    ('FEMALE', 'female'),
)

DISEASE_CHOICES = (
    ('Malaria', 'malaria' ),
    ('Tuberculosis', 'tuberculosis' ),
)

BOOLEAN_CHOICES = (
    ('Y', 'yes'),
    ('N', 'no'),
)

MEDICINE_CHOICES = (
    ('Doxycycline', 'doxycycline'),
    ('Lariam', 'lariam'),
    ('Malarone', 'malarone'),
    ('Rifater', 'rifater'),
    ('Ethambutol', 'ethambutol'),
    ('Isoniazid', 'isoniazid'),
)

# model: Patient
# fields: id, first_name, last_name, gender, age, phone_number, created_at
class Patient(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    age = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "%s %s" %(self.first_name, self.last_name)

    def get_absolute_url(self):
        return reverse('patients-list')

# model: PatientDetail
# fields: id, patient, disease_identified, weight, alcoholic,
# pregnant, breast_feeding, liver_disease, eye_disease, kidney_disease, diabetes, medicine
class PatientDetail(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    disease_identified = models.CharField(max_length=20, choices=DISEASE_CHOICES)
    weight_in_kg = models.IntegerField()
    alcoholic = models.CharField(max_length=1, choices=BOOLEAN_CHOICES)
    pregnant = models.CharField(max_length=1, choices=BOOLEAN_CHOICES)
    breast_feeding = models.CharField(max_length=1, choices=BOOLEAN_CHOICES)
    liver_disease = models.CharField(max_length=1, choices=BOOLEAN_CHOICES)
    eye_disease = models.CharField(max_length=1, choices=BOOLEAN_CHOICES)
    kidney_disease = models.CharField(max_length=1, choices=BOOLEAN_CHOICES)
    diabetes = models.CharField(max_length=1, choices=BOOLEAN_CHOICES)
    medicine = models.CharField(max_length=20, blank=True, choices=MEDICINE_CHOICES)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "%s details" %(self.patient)
