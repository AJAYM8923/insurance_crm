from django.db import models
from django.contrib.auth.models import User

class Agent(models.Model):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, unique=True)
    address = models.TextField()
    dob = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES,default='Male')
    profile_picture = models.ImageField(upload_to='agents/', null=True, blank=True)

    def __str__(self):
        return self.user.get_full_name()

class Campaign(models.Model):
    name = models.CharField(max_length=100, unique=True)
    date = models.DateField()
    location = models.CharField(max_length=255)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Client(models.Model):
    MARITAL_CHOICES = [('Single', 'Single'), ('Married', 'Married')]
    YES_NO = [('Yes', 'Yes'), ('No', 'No')]
    SOURCES = [('Friend', 'Friend'), ('Social Media', 'Social Media'), ('Other', 'Other')]
    POLICIES = [
        ('Car Insurance', 'Car Insurance'),
        ('Health Insurance', 'Health Insurance'),
        ('Travel Insurance', 'Travel Insurance')
    ]

    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)

    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    email = models.EmailField()
    address = models.TextField()
    age = models.PositiveIntegerField()
    dob = models.DateField()
    qualification = models.CharField(max_length=100)
    profession = models.CharField(max_length=100)
    aadhar = models.CharField(max_length=14)
    pan = models.CharField(max_length=14)
    income = models.DecimalField(max_digits=10, decimal_places=2)

    marital_status = models.CharField(max_length=10, choices=MARITAL_CHOICES)
    have_kids = models.CharField(max_length=3, choices=YES_NO)
    know_about_us = models.CharField(max_length=20, choices=SOURCES)

    existing_profile = models.CharField(max_length=3, choices=YES_NO)
    customer_service = models.TextField()
    claim_satisfaction = models.TextField()
    visited_policy = models.CharField(max_length=100, choices=POLICIES)

    willingness_to_purchase = models.CharField(max_length=3, choices=YES_NO)
    willingness_to_share_prev = models.CharField(max_length=3, choices=YES_NO)
    prev_insurance_number = models.CharField(max_length=100, blank=True, null=True)
    prev_insurance_name = models.CharField(max_length=100, blank=True, null=True)
    prev_insurance_claimed = models.CharField(max_length=3, choices=YES_NO)
    willingness_to_switch = models.CharField(max_length=3, choices=YES_NO, default='No')

    preferences = models.TextField()
    agent_note = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.phone}"
