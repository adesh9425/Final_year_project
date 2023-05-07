from django.db import models

# Create your models here.


from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import models
from django.core.validators import RegexValidator
from django.db import models





class Doctor(models.Model):
	email= models.EmailField()
    #phone= models.CharField(max_length=17) 
	name=models.CharField(max_length=10)
	row_status=models.BooleanField(default=True) 
    
class User(models.Model):
	name=models.CharField(max_length=10)
	email= models.EmailField()
    #phone= models.CharField(max_length=17) 
	disease=models.CharField(max_length=10)
	dob=models.DateField()
	city=models.CharField(max_length=10)
	assigned_doctor=models.ForeignKey(Doctor, on_delete=models.CASCADE)
	row_status=models.BooleanField(default=True)
	

class Health(models.Model):
	timestamp=models.DateTimeField(max_length=10)
	name= models.ForeignKey(User, on_delete=models.CASCADE)
	temperature=models.FloatField(max_length=4)
	pulse=models.FloatField(max_length=4)  
    
    
        
class Admin(models.Model):
    username=models.CharField(max_length=10)
    password=models.CharField(max_length=10)
    

