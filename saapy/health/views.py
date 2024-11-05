import matplotlib
# Create your views here.
from django.shortcuts import render
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
import urllib, base64
from rest_framework import viewsets
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import get_object_or_404
import requests
import json
import datetime
from django.contrib import messages
from time import strptime
import os
import glob
import time
import collections
import subprocess
from django.http import HttpResponse
from io import BytesIO
from django.contrib import auth
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .serializers import * 
from django.urls import reverse
import io
from django.http import HttpResponse
from django.shortcuts import render
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Health, User
import seaborn as sns
matplotlib.use('Agg')
# Create your views here.


class HealthViewSet(viewsets.ModelViewSet):
	queryset=Health.objects.all()
	serializer_class=HealthSerializer

@cache_control(no_cache=True, must_revalidate=True)
def func():
  #some code
	return
@login_required
def home(request):
    r = requests.get('http://127.0.0.1:8000/health/')
    result = r.text
    output = json.loads(result)
    users = User.objects.all()

    table = []
    for user in users:
        user_data = Health.objects.filter(name_id=user.id).order_by('-timestamp')
        if user_data:
            user_data = user_data.first()
            table.append({'name': user.name, 'temperature': user_data.temperature, 'pulse': user_data.pulse})
        else:
            table.append({'name': '','temperature': '', 'pulse':''})
    
    k={'users':table}
    return render(request, 'index.html', k)

	#return render(request,('testhtml.html',{'timestamp':timestamp,'name':name,'temperature':temperature,'pulse':pulse})
	#return render(request,('index.html',{'healthdata':result})

@login_required

def archive(request):
    list = []
    d = {'item': {}, 'details': {}}
    if 'Patient_Name' in request.GET:
        last_patient = request.GET['Patient_Name']

        
        r = requests.get('http://127.0.0.1:8000/health/')
        count = 1
        c = 0
        x = int(count) - 1
    
        user = User.objects.filter(name=last_patient).all()
        for i in user:
            fulldata = Health.objects.filter(name_id=i.id).all()
    
        for i in fulldata:
            d['item']['timestamp'] = i.timestamp
            d['item']['temperature'] = i.temperature
            d['item']['pulse'] = i.pulse
            list.append(d['item'])
        for user in user:
            d['details']['name'] = user.name
            d['details']['email'] = user.email
            d['details']['dob'] = user.dob
            d['details']['disease'] = user.disease
            d['details']['city'] = user.city
            d['details']['doctor'] = user.assigned_doctor.name
            d={'items':list,'details':d['details']}
    return render(request, 'archivetest.html', d)

@login_required()
@csrf_exempt
@cache_control(no_cache=True, must_revalidate=True)
def send_email(request):
    pass

@login_required()
@csrf_exempt

@cache_control(no_cache=True, must_revalidate=True)
def generate_chart(request):
    if request.method == 'POST':
        # Get the form data
        name = request.POST['name']
        chart_type = request.POST['chart-type']
        user = User.objects.filter(name=name).first()

        if user:
            health = Health.objects.filter(name_id=user.id)
            time, temp, pulse = [], [], []

            for record in health:
                time.append(record.timestamp)
                temp.append(record.temperature)
                pulse.append(record.pulse)

            # Initialize the figure and subplots
            fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)

            # Temperature plot based on chart type
            if chart_type == 'line':
                sns.lineplot(x=time, y=temp, ax=ax1, color='red')
                sns.scatterplot(x=time, y=temp, ax=ax1)
            elif chart_type == 'pi':
                fig, (ax1, ax2) = plt.subplots(1, 2)  # New layout for pie chart
                high_temp = sum(1 for t in temp if t > 98)
                ok_temp = sum(1 for t in temp if t == 98)
                low_temp = sum(1 for t in temp if t < 98)
                ax1.pie([high_temp, ok_temp, low_temp], labels=['High', 'OK', 'Low'], colors=['red', 'green', 'yellow'],
                        autopct='%1.1f%%')
            elif chart_type == 'hist':
                sns.histplot(data=temp, color='blue', bins=5, ax=ax1)
            elif chart_type == 'box':
                sns.boxplot(x=temp, palette='Set3', ax=ax1)

            ax1.set_ylabel('Temperature (°C)')

            # Pulse plot based on chart type
            if chart_type == 'line':
                sns.lineplot(x=time, y=pulse, ax=ax2, color='blue')
                sns.scatterplot(x=time, y=pulse, ax=ax2, color='red')
            elif chart_type == 'pi':
                high_pulse = sum(1 for p in pulse if p > 72)
                ok_pulse = sum(1 for p in pulse if p == 72)
                low_pulse = sum(1 for p in pulse if p < 72)
                ax2.pie([high_pulse, ok_pulse, low_pulse], labels=['High', 'OK', 'Low'],
                        colors=['red', 'green', 'yellow'], autopct='%1.1f%%')
            elif chart_type == 'hist':
                sns.histplot(data=pulse, color='red', bins=5, ax=ax2)
            elif chart_type == 'box':
                sns.boxplot(x=pulse, palette='Set3', ax=ax2)

            ax2.set_ylabel('Pulse (bpm)')
            ax2.set_xlabel('Time')

            fig.suptitle('Temperature and Pulse vs Time')

            # Save the chart to a buffer
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)

            # Convert the buffer to an image for rendering in HTML
            image_png = buffer.getvalue()
            buffer.close()
            image = base64.b64encode(image_png).decode()
            img_src = f'data:image/png;base64,{image}'

            # Render the HTML page with the chart
            return render(request, 'statistics.html', {'img_src': img_src})

    return render(request, 'statistics.html')
@login_required
def pdetails(request):
	msg=""
	return render(request,'form.html',{'msg':msg})
@login_required
def formsubmit(request):
    if request.user.is_authenticated:
        if 'InputName' in request.GET:
            patientName = request.GET['InputName']
            email = request.GET['InputEmail']
            assigned_to = request.GET['Inputassigned_to']
            disease = request.GET['Inputdisease']
            dob = request.GET['Inputdob']
            city = request.GET['InputCity']
        doc=get_object_or_404(Doctor, id=assigned_to)
        user=User(name=patientName,email=email,assigned_doctor=doc,dob=dob,disease=disease,city=city)
        user.save()
        print ("patient name : ",patientName)
        
        messages.success(request,"Patient Created Successfully")
        return render(request,'form.html',{})
    else: 
        return render(request,'login.html',{})

def logindetails(request):
	masg=""
	return render(request,'login.html',{'masg':masg})


def logout(request):
	auth.logout(request)
	return render(request,'login.html',{})
	
def login2(request):
	username=""
	if 'Username' in request.GET:
		username=request.GET['Username']
		password=request.GET['Password']
	#print "username :",username,password
	'''
	user = authenticate(username=username, password=password)
	if user:
		if user.is_active:
			login(request, user)
			return render(request,('form.html',{})
		else:
			return HttpResponse("Account disables")
	else:
		print "invalise login"
		return HttpResponse("Invalid Login")
	'''
	
	#cur.execute("SELECT password from admin where username=%s",username)
	row=Admin.objects.filter(username=username).fetchone().values()
	while row is not None:
		print( row[0])
		print (password)
		if row[0]==password:
			print ("login success")
			return render(request,'form.html',{})
		else:
			print ("login failed")
			return render(request,'archive.html',{})
	
def login(request):
	c={}
	c.update(csrf(request))
	return render(request,'login.html',c)

def invalid_login(request):
	messages.error(request,"Invalid Credentials.Please try again..!!")
	return render(request,'login.html',{})
def auth_view(request):
    username = request.POST.get('Username', '')
    password = request.POST.get('Password', '')
    print("user ", username)
    user = auth.authenticate(username=username, password=password)
    if user is not None:
        auth.login(request, user)
        return render(request,'form.html', {})
    else:
        messages.error(request, "Invalid Credentials.Please try again..!!")
        return render(request, 'login.html', {})
    

