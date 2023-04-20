from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import models
from django.core.validators import RegexValidator
from django.db import models



def validate_my_email(value):
    if not value.endswith('@example.com'):
        raise ValidationError('Email must be from example.com domain')

class user(model.Model):
	
	id=models.AutoField(primary_key=True)
	name=models.CharField(max_length=10)
	email= models.EmailField(validators=[validate_email, validate_my_email])
	phone_regex = RegexValidator(regex=r'^\+?91?\d{10}$', message="Phone number must be in the format: '+91xxxxxxxxxx'. Up to 15 digits allowed.")
    	phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True) # validators should be a list
	disease=models.CharField(max_length=10)
	dob=models.DateField()
	city=models.CharField(max_length=10)
	assigned_doctor=models.ForeignKey(doctor, on_delete=models.CASCADE)
	row_status=models.BooleanField(default=True)
	
class doctor(model.Model):
	id=models.AutoField(primary_key=True)
	email= models.EmailField(validators=[validate_email, validate_my_email])
	phone_regex = RegexValidator(regex=r'^\+?91?\d{10}$', message="Phone number must be in the format: '+91xxxxxxxxxx'. Up to 15 digits allowed.")
    	phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True) # validators should be a list
	name=models.CharField(max_length=10)
	row_status=models.BooleanField(default=True)

class health(models.Model):
	timestamp=models.DateTimeField(max_length=10)
	id= models.ForeignKey(user, on_delete=models.CASCADE)
	temperature=models.FloatField(max_length=4)
	pulse=models.FloatField(max_length=4)
