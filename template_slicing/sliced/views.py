from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ValidationError
# from . models import user, services, sub_services, appointment
from .models import * 


# Create your views here.
def index(request):
    serviceCount = services.objects.all().count()
    subServiceCount = sub_services.objects.all().count()
    bookingCount = appointment.objects.all().count()
    return render(request, 'sliced/home.html', {'serviceCount': serviceCount, 'subServiceCount': subServiceCount, 'bookingCount': bookingCount})

def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username,
        password=password)
        # Check if authentication successful
        if user is not None:
            if user.is_superuser:
                login(request, user)
                return HttpResponseRedirect(reverse("home"))
            else:
                return render(request, "sliced/login.html", {
            "message": "Invalid username and/or password."
        })
        else:
            return render(request, "sliced/login.html", {
            "message": "Invalid username and/or password."
        })
    else:
        return render(request, "sliced/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))

def add_service(request):
    if request.method =="POST":
        serName = request.POST['name']
        try:
            obj = services(name = serName)
            obj.save()
            return HttpResponseRedirect(reverse('allServices'))
        except:
            return render(request, 'sliced/add_services.html', {'msg': 'Service already exists.'})
    else:
        return render(request, 'sliced/add_services.html')   

def allServices(request):
    allSer = services.objects.all()
    return render(request, 'sliced/table.html', {'data': allSer})


def deletetables(request,id):
    # table = allServices.objects.get(id = table)
    selService = services.objects.get(id = id)
    selService.delete()
    return HttpResponseRedirect(reverse('allServices'))

def edittables(request,id):
    selService = services.objects.get(id = id)

    if request.method == "POST":
        service = request.POST['name']

        selService.name = service
        try:
            selService.save()
            return HttpResponseRedirect(reverse('allServices'))
        except:
            return render (request, 'sliced/editService.html',{'data':selService, 'msg': 'service already exists.'})
    else:
        return render (request, 'sliced/editService.html',{'data':selService})

def addsubServices(request):
    subSer = services.objects.all()
    if request.method == 'POST':
        ser = request.POST['serv']
        selServ = services.objects.get(id = ser)

        name = request.POST['name']
        price = request.POST['price']
        img = request.FILES['images']
        desc = request.POST['desc']

        a = sub_services(service_id = selServ, name = name, price = price, image = img, description = desc)
        try:
            a.save()
            return HttpResponseRedirect(reverse('allsubServices'))
        except:
            return render(request, 'sliced/sub_services.html', {'data': subSer, 'msg': 'Subservice already exists.'})

    else:
        return render(request, 'sliced/sub_services.html', {'data': subSer})

def allsubServices(request):
    allsubSer = sub_services.objects.all()
    return render(request, 'sliced/tablesubservices.html', {'data': allsubSer})

def deleteSubService(request,id):
    # table = allServices.objects.get(id = table)
    subService = sub_services.objects.get(id = id)
    subService.delete()
    return HttpResponseRedirect(reverse('allsubServices'))

def editSubService(request,id):
    subService = sub_services.objects.get(id = id)
    servData = services.objects.all()
    if request.method == "POST":
        ser = request.POST['serv']
        selServ = services.objects.get(id = ser)

        name = request.POST['name']
        price = request.POST['price']
        img = request.FILES.get('images')

        if img is not None:
            subService.image = img


        subService.service_id = selServ
        subService.name = name
        subService.price = price
        subService.save()
        return HttpResponseRedirect(reverse('allsubServices'))
    else:
        return render (request, 'sliced/editsubservices.html',{'data':subService, 'service': servData})


def allOrders(request):
    data = appointment.objects.all()
    return render(request, 'sliced/allBooking.html', {'data': data})

def updateOrder(request, id, type):
    orderData = appointment.objects.get(id = id)
    orderData.status = type
    orderData.save()
    return HttpResponseRedirect(reverse('allBooking'))