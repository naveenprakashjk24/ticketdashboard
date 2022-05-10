
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from .forms import LoginForm, SignUpForm
from .models import RequestTicket, Incident_Category, Tech_User, Notes, Status, Priority,Service_Category
from django.contrib.auth.models import User
from django.db.models import Q

@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))



def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})

def logoutUser(request):
    logout(request)
    return redirect("accounts/login.html")


def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)

            msg = 'User created - please <a href="/login">login</a>.'
            success = True

            # return redirect("/login/")

        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})


def requestpage(request):
    
    tickets= RequestTicket.objects.all()
    incident_category = Incident_Category.objects.all()
    service_category = Service_Category.objects.all()
    user_list = Tech_User.objects.all()
    status = Status.objects.all()
    
    
    if request.method=="POST":
        RequestTicket.objects.create(
            subject = request.POST.get('subject'),
            description = request.POST.get('description'),
            insident_category =  request.POST.get('insident_category'),
            service_category= request.POST.get('service_category'),
            created_by = request.user,
            county = request.POST.get('county'),
            area = request.POST.get('area'),
            city = request.POST.get('city'),
            pin_code = request.POST.get('pin_code'),
            assigned_to = request.POST.get('assigned_to')
            
            
            
        )
    context = {'tickets':tickets ,'status':status,'service_category':service_category,'incident_category':incident_category,'user_list':user_list }
    
    return render(request, 'home/request-page.html',context)


def settingpage(request):
    
    if request.method=='POST':
        if request.POST.get('statusname'):
            Status.objects.create(
                name=request.POST.get('statusname')
            )
            return redirect('setting')
   
        elif request.POST.get('priorityname'):
            Priority.objects.create(
                name=request.POST.get('priorityname')
            )
            return redirect('setting')
        elif request.POST.get('servicectg'):
            Service_Category.objects.create(
                name=request.POST.get('servicectg')
            )
            return redirect('setting')
        elif request.POST.get('incidentctg'):
            Incident_Category.objects.create(
                name=request.POST.get('incidentctg')
            )
            return redirect('setting')
        elif request.POST.get('username') or request.POST.get('userno'):
            Tech_User.objects.create(
                name=request.POST.get('username'),
                contact_mo = request.POST.get('userno'),
                role=request.POST.get('role')
                
            )
            return redirect('setting')
        
    
    priority = Priority.objects.all()
    service_category = Service_Category.objects.all()
    incident_category = Incident_Category.objects.all()
    user_list = Tech_User.objects.all()
    status = Status.objects.all()
    context = {'status':status, 'priority':priority,'service_category':service_category,'incident_category':incident_category,'user_list':user_list }
    return render(request, 'home/settings-page.html', context)

def deleteStatus(request,pk):
    status = Status.objects.get(id=pk)
    if request.method =='POST':
        status.delete()
        return redirect('setting')
    
    return render(request, 'home/delete-page.html', {'obj':status})


def deleteService(request,pk):
    service_category = Service_Category.objects.get(id=pk)
    if request.method =='POST':
        service_category.delete()
        return redirect('setting')
    
    return render(request, 'home/delete-page.html', {'obj':service_category})


def deleteIncident(request,pk):
    incident_category = Incident_Category.objects.get(id=pk)
    if request.method =='POST':
        incident_category.delete()
        return redirect('setting')
    
    return render(request, 'home/delete-page.html', {'obj':incident_category})


def deletePriority(request,pk):
    priority = Priority.objects.get(id=pk)
    if request.method =='POST':
        priority.delete()
        return redirect('setting')
    
    return render(request, 'home/delete-page.html', {'obj':priority})


def deleteTechuser(request,pk):
    userlist = Tech_User.objects.get(id=pk)
    if request.method =='POST':
        userlist.delete()
        return redirect('setting')
    
    return render(request, 'home/delete-page.html', {'obj':userlist})


def changesPage(request):
    return render(request, 'home/changes-page.html')

def knowladgePage(request):
    return render(request, 'home/knowladge-page.html')

def requestDetailPage(request, pk):
  
    ticket_details = RequestTicket.objects.get(id=pk)
    notes_detail = ticket_details.notes_set.all()
    if request.method =="POST":
        notes = Notes.objects.create(
            user=request.user,
            note = request.POST.get('body'),
            ticket=ticket_details
        )
    context = {"ticket_details":ticket_details,"notes_detail":notes_detail}
    return render (request,'home/ticket-detail.html', context)