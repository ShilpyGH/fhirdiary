
from django.db import models

class AppUser(models.Model):
    user_id = models.IntegerField()
    first_name = models.CharField(max_length=200)
    middle_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.CharField(max_length=250)
    user_name = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    user_type = models.IntegerField()

class UserType(models.Model):
    user_type_id = models.IntegerField()
    user_type = models.CharField(max_length=200)

class Patient(models.Model):
    patient_id = models.IntegerField()
    user_id = models.ForeignKey(AppUser)
    dob = models.DateField()
    gender = models.CharField(max_length=2)
    address = models.CharField(max_length=300)
    phone = models.CharField(max_length=20)
    height = models.IntegerField()
    weight = models.IntegerField()
    #care_partner_id = models.ForeignKey(CarePartner)

class CarePartner(models.Model):
    care_partner_id = models.IntegerField()
    user_id = models.ForeignKey(AppUser)
    relationship_type = models.CharField(max_length=200)
    patient_id = models.ForeignKey(Patient)

class CareProvider(models.Model):
    provider_id = models.IntegerField()
    provider_f_name = models.CharField(max_length=200)
    provider_m_name = models.CharField(max_length=200)
    provider_l_name = models.CharField(max_length=200)
    patient_id = models.ForeignKey(Patient)

class Entry(models.Model):
    entry_id = models.IntegerField()
    user_id = models.ForeignKey(AppUser)
    patient_id = models.ForeignKey(Patient)
    date_time = models.DateTimeField()
    comments = models.CharField(max_length=250)

class headache(models.Model):
    headache_id = models.IntegerField()
    entry_id = models.ForeignKey(Entry)
    time_headache = models.DateTimeField()
    pain_severity = models.IntegerField()
    location = models.CharField(max_length=50)
    pain_type = models.CharField(max_length=150)

class Triggers(models.Model):
    trigger_id = models.IntegerField()
    name_trigger = models.CharField(max_length=100)
    snomed_code = models.CharField(max_length=50)

class TriggerEntry(models.Model):
    trigger_entry_id = models.IntegerField()
    trigger_id = models.ForeignKey(Triggers)
    entry_id = models.ForeignKey(Entry)
    time_trigger = models.DateTimeField()

class MedicationRequest(models.Model):
    med_id = models.IntegerField()
    snomed_code = models.CharField(max_length=50)
    drug_name = models.CharField(max_length=250)
    med_strength = models.CharField(max_length=250)

class RescueMeds(models.Model):
    res_med_id = models.IntegerField()
    entry_id = models.ForeignKey(Entry)
    med_id = models.ForeignKey(MedicationRequest)
    time = models.DateTimeField()
    pill_count = models.IntegerField()
