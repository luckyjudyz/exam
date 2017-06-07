from django.shortcuts import render,  HttpResponse, redirect
from django.contrib import messages
from .models import UserDB, TravelDB
from django.db.models import Q

# Create your views here.
def index(request):
    return render(request, "exam_app/index.html")

def log_register(request):
    if request.method == "POST":
        print request.POST["type"] * 10
        if request.POST["type"] == 'Register':
            response = UserDB.objects.check_create(request.POST)
        elif request.POST['type'] == "Login":
            response = UserDB.objects.check_log(request.POST)
        if not response[0]:
            for message in response[1]:
                messages.error(request, message[1])
            return redirect('exam_app:index')
        else:
            request.session['user'] = {
            "id":response[1].id,
            'name': response[1].name,
            }
            return redirect('exam_app:travel')
    return redirect('exam_app:index')

def logout(request):
	request.session.clear()
	return redirect('exam_app:index')

def travel(request):
    my_plans = TravelDB.objects.filter(Q(planuser=UserDB.objects.get(id=request.session['user']['id'])) | Q(joinusers=UserDB.objects.get(id=request.session['user']['id'])))
    other_plans = TravelDB.objects.exclude(planuser=UserDB.objects.get(id=request.session['user']['id']))
    # my_plans = sorted(my_plans, key=lambda x: x.startdate, reverse = False)
    # other_plans = sorted(other_plans, key=lambda x: x.startdate, reverse = False)
    print request.session['user']['name']
    print request.session['user']['name']
    print request.session['user']['name']
    print request.session['user']['name']
    print request.session['user']['name']

    context = {
    "my_plans": my_plans,
    "other_plans": other_plans
    }
    return render(request,'exam_app/travel.html',context)

def addtravel(request):
    return render(request,'exam_app/add.html')

def add(request):
    response = TravelDB.objects.add(request.POST,request.session['user']['id'])
    if not response[0]:
        for message in response[1]:
            messages.error(request, message[1])
        return redirect('exam_app:addtravel')
    else:
        return redirect('exam_app:travel')

def join(request,id):
    TravelDB.objects.join(id,request.session['user']['id'])
    return redirect('exam_app:travel')

def destination(request,id):
    travel=TravelDB.objects.get(id=id)
    joinusers=travel.joinusers
    context={
    'travel':travel
    }
    return render(request,'exam_app/destination.html',context)
