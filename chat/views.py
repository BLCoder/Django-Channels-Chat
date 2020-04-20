from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .forms import registerUser
import json
from .models import Profile

@login_required(login_url='/chat/login')
def index(request):
	if request.method=="POST":
		room_name=request.POST.get("room-name")
		return redirect(room,room_name=room_name)

	return render(request, 'chat/index.html')

@login_required(login_url='/chat/login')
def room(request, room_name):
	users=User.objects.all()
	return render(request, 'chat/room.html', {'room_name_json': mark_safe(json.dumps(room_name)),'username': mark_safe(json.dumps(request.user.username)),'users':users})


def getLogin(request):
	if request.user.is_authenticated:
		return redirect('index')
	if request.method=="POST":
		#user=request.POST.get('user')
		user=request.POST['user']
		password=request.POST.get('pass')
		auth=authenticate(request,username=user,password=password)
		if auth is not None:
			login(request,auth)
			return redirect('index')
	return render(request,'auth/login.html')


def getlogout(request):
	logout(request)
	return redirect('login')


def getRegister(request):
	if request.user.is_authenticated:
		return redirect('index')
	form=registerUser(request.POST or None)
	if form.is_valid():
		instance=form.save(commit=False)
		instance.save()
		return redirect('login')
	return render(request,'auth/register.html',{'form':form})