from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
import json

# from . models import user, services, sub_services, appointment
from sliced.models import * 
# Create your views here.
def index(request):
    print(f'user {request.user}')
    if request.user != 'AnonymousUser':
        request.session["cart"] = []
    return render(request, 'user_module/home.html')

def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username,
        password=password)
        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "user_module/login.html", {
            "msg": "Invalid username and/or password."
        })
    else:
        return render(request, "user_module/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('logins'))

def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        #Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "user_module/register.html",{"msg": "Passwords must match."})

        #Attempt to create new user
        try:
            users = user.objects.create_user(username,email,password)
            users.save()
            print(users)
        except IntegrityError:
            return render(request, "user_module/register.html",{"msg": "Username already taken."})

        return render(request, "user_module/register.html",{"msg": 'Registered successfully.'})

    else:
        return render(request, "user_module/register.html")

def main(request):
    return render(request, 'user_module/home.html')


def subService(request, id):
    selService = services.objects.get(id = id)
    data = sub_services.objects.filter(service_id = selService)
    return render(request, 'user_module/subServices.html', {'data': data, 'service': selService})


@login_required(login_url='/user/logins')
def addToCart(request, subId):
    # a =  next((i for i,d in enumerate(request.session['cart']) if str(subId) in d), None)
    # print(a)
    # if a:
    #     print('yay')
    #     request.session['cart'][a][str(subId)] = request.session['cart'][a][str(subId)] + 1
    #     print(request.session['cart'])

    # else:
    #     b = dict()
    #     b[subId] = 1
    #     request.session['cart'] += [b]
    #     print(request.session['cart'])
    # data = sub_services.objects.get(id = subId)
    request.session['cart'] += [subId]
    print(request.session['cart'])
    serviceId = sub_services.objects.get(id = subId).service_id.id
    return HttpResponseRedirect(reverse('subService', kwargs={'id': serviceId}))

@login_required(login_url='/user/logins')
def viewCart(request):
    print(request.session['cart'])
    if len(request.session['cart']) > 0:
        print(request.session['cart'])
        uniqueItem = list(set(request.session['cart']))
        print(uniqueItem)
        a = []
        sums = 0
        for i in uniqueItem:
            cartDict = dict()
            cartDict['item'] = sub_services.objects.get(id = i)
            cartDict['quant'] = 1
            cartDict['total'] = int(sub_services.objects.get(id = i).price) * 1
            sums += cartDict['total']
            a.append(cartDict)
        
        print(a)


        return render(request, 'user_module/viewCart.html', {'cart': a, 'checkout': sums})
    else:
        return render(request, 'user_module/viewCart.html', {'msg': 'Empty Cart'})

def removeItemCart(request, id):
    a = request.session['cart']
    a = list(filter((id).__ne__, a))
    print(a)
    request.session['cart'] = a

    return HttpResponseRedirect(reverse('viewCart'))

def allOrders(request):
    data = appointment.objects.filter(user_id = request.user).order_by('bookingdate')
    return render(request, 'user_module/allOrder.html', {'data': data})

def checkOut(request):
    try:
        if request.method == 'POST':
            date = request.POST['dates']
        for i in list(set(request.session['cart'])):
            b = sub_services.objects.get(id = i)
            a = appointment(user_id = request.user, subservice_id = b, bookingdate = date)
            a.save()
        request.session['cart'] = []
        return HttpResponseRedirect(reverse('allOrders'))
    except:
        return HttpResponseRedirect(reverse('index'))