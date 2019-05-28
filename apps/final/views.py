from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User, Trip

# Create your views here.
def index(request):
  return render(request, 'final/index.html')

def register(request):
  if request.method == "POST":
    errors = User.objects.validation(request.POST)
    if len(errors) > 0:
      for key, value in errors.items():
        messages.error(request, value)
      return redirect('/')
    else:
      new_id = User.objects.register(request.POST)
      request.session['user_id'] = new_id
      return redirect('/dashboard')

def displaytrip(request, my_val):
  print(my_val)
  context = {
    "trips": Trip.objects.get(id=my_val)
  }
  return render(request, 'final/details.html', context)

def dashboard(request):
  if not 'user_id' in request.session:
    return redirect('/')
  else:
    context ={
      "user_info": User.objects.get(id=request.session['user_id']),
      "trips": Trip.objects.filter(created_by_id=request.session['user_id']),
      "othertrips": Trip.objects.exclude(created_by_id=request.session['user_id']),
      "joined": Trip.objects.filter(join__id=request.session['user_id'])
    }


    return render(request, 'final/dashboard.html', context)

def logout(request):
  del request.session['user_id']
  return redirect('/')

def login(request):
  if request.method == "POST":
    errors = User.objects.login_validation(request.POST)
    if len(errors) > 0:
      for key, value in errors.items():
        messages.error(request, value)
      return redirect('/')
    else:
      user_info = User.objects.get(username=request.POST['login_user'])
      request.session['user_id'] = user_info.id
      return redirect('/dashboard')

def addplan(request):
  return render(request, 'final/addplan.html')

def jointrip(request, my_val):
  user = User.objects.get(id=request.session['user_id'])
  trip = Trip.objects.get(id=my_val)

  trip.join.add(user)
  return redirect('/trips/' + my_val)


def addtrip(request):
  if request.method == "POST":
    errors = User.objects.trip_validation(request.POST)
    if len(errors) > 0:
      for key, value in errors.items():
        messages.error(request, value)
      return redirect('/addplan')
    else:
      poster = User.objects.get(id=request.session['user_id'])
      Trip.objects.create(destination=request.POST['destination'], description=request.POST['description'], datefrom=request.POST['datefrom'], dateto=request.POST['dateto'], created_by=poster)
      return redirect('/dashboard')