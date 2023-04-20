from django.db import models

class user(model.Model):
	id=models.AutoField(primary_key=True)
	name=models.CharField(max_length=10)
	disease=models.CharField(max_length=10)
	dob=models.DateField()
	city=models.CharField(max_length=10)
	assigned_doctor=models.ForeignKey(doctor, on_delete=models.CASCADE)
	row_status=models.BooleanField(default=True)
	
class doctor(model.Model):
	id=models.AutoField(primary_key=True)
	name=models.CharField(max_length=10)
	row_status=models.BooleanField(default=True)

class health(models.Model):
	timestamp=models.DateTimeField(max_length=10)
	id= models.ForeignKey(user, on_delete=models.CASCADE)
	temperature=models.FloatField(max_length=4)
	pulse=models.FloatField(max_length=4)
