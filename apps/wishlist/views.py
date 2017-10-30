from django.shortcuts import render
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.db.models import Count
from .models import User, Wish
from django.core.exceptions import ObjectDoesNotExist
import time
import re
import datetime
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your views here.
def index(request):
    return render(request, "wishlist/index.html")

def register(request):
    logged = True
    if len(request.POST["name"]) < 2:
        messages.error(request, "The Name Field must have at least 2 characters")
        logged = False
    if request.POST["name"].isalpha() == False: 
        messages.error(request, "Your name can only have letters")
        logged = False
    if not EMAIL_REGEX.match(request.POST["email"]):
        messages.error(request, "Please enter a valid email address")
        logged = False  
    if len(request.POST["password"]) < 8:
        messages.error(request, "Your password must contain at least 8 characters")
        logged = False  
    if request.POST["password"] != request.POST["confirm_password"]:
        messages.error(request, "Your passwords didn't match")
        logged = False
    if len(request.POST["date_of_birth"]) < 1:
        messages.error(request, "Date of Birth Field cannot be empty")     
        logged = False
    if not logged:
        return redirect ("/")     
    
    User.objects.create(name=request.POST["name"], password=request.POST["password"], email=request.POST["email"], date_of_birth=request.POST["date_of_birth"])
    request.session["current_user"] = User.objects.get(email=request.POST["email"]).id
    return redirect("/dashboard")

def login(request):
    try:
        users = User.objects.get(email=request.POST["email"], password=request.POST["password"])
    
    except ObjectDoesNotExist:
        messages.error(request, "Invalid username or password")
        return redirect("/")    
    
    else:
        context = {}
        request.session["current_user"] = User.objects.get(email=request.POST["email"], password=request.POST["password"]).id
        if "current_user" in request.session.keys():
            return redirect("/dashboard")
def dashboard(request):
    if "current_user" in request.session.keys():
        user = User.objects.get(pk = request.session["current_user"])
        wishes = Wish.objects.all()
        my_wishes = user.items.all()
        wishes = Wish.objects.exclude(id__in=my_wishes)
	
        context = {
        "user": user,
        'wishes': wishes,
        'my_wishes': my_wishes,
        }
    return render(request, "wishlist/dashboard.html", context)

def added(request):
    if "current_user" in request.session.keys():
        user = User.objects.get(pk = request.session["current_user"])
        context = {
        "user": user
        }
    return render(request, "wishlist/added.html", context)

def submitted(request):
    wishes = Wish.objects.create(user_id=(User.objects.get(pk=request.session["current_user"])).id, item = request.POST["item"])
    user = User.objects.get(pk = request.session["current_user"])
    user.items.add(wishes)
    return redirect("/dashboard")

def addWish(request, id):
	if "current_user" in request.session.keys():
		user = User.objects.get(pk = request.session["current_user"])
		wish = Wish.objects.get(id = id)
		wish.wishers.add(user)
		return redirect("/dashboard")

def removeWish(request, id):
	if "current_user" in request.session.keys():
		user = User.objects.get(pk = request.session["current_user"])
		wish = Wish.objects.get(id = id)
		wish.wishers.remove(user)
		return	redirect("/dashboard")

def item(request, id):
	if "current_user" in request.session.keys():
		user = User.objects.get(pk = request.session["current_user"])
		context = {
		"user": user,
		"wish": Wish.objects.get(id = id)		
		}
	return render(request, "wishlist/item.html", context)

def delete(request, id):
    wish = Wish.objects.get(id = id)
    wish.delete()
    return redirect("/dashboard")

def logout(request):
    request.session.clear()
    messages.add_message(request, messages.INFO, "Successfully logged out")
    return render(request, "wishlist/index.html")