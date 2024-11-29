from django.shortcuts import render

# Create your views here.
import re
import json
import time, threading
import psutil
from datetime import datetime
from django.http import HttpResponse
from mys.forms import LogMessageForm
from mys.models import LogMessage
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import login, authenticate
import os, shutil
from django.conf import settings
from django.core.files.storage import default_storage

from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from mys.forms import SignUpForm
from .models import CustomUser
from mys.MYSMain import setupMain, progPrint
#from wsgiref.util import 





#def home(request):
#    return render(request, "mys/home.html")

class HomeListView(ListView):
    """Renders the home page, with a list of all messages."""
    model = LogMessage

    def get_context_data(self, **kwargs):
        context = super(HomeListView, self).get_context_data(**kwargs)
        return context    

def about(request):
    return render(request, "mys/about.html")

def ProcessOptionChange(request):
    if request.is_ajax():
        if request.method == 'POST':
            # The next line creates an object that points to the user row in the database.
            # The object, called database_User, can now be written to and updated using save().
            database_User = CustomUser.objects.get(username= request.user.username)
            print ("Raw Data: ", request.body)
            result_obj = json.loads(request.body)
            if (result_obj["Result1"]=="0"):
                database_User.mode = "all"
            if (result_obj["Result1"]=="1"):
                database_User.mode = "highlighted"    
            database_User.save()        
        return HttpResponse("OK")
    else:    
        return HttpResponse(status = 500)


@csrf_protect
def FileUpload(request):
    FileContainer = request.FILES
    #print(FileContainer)
    student_files_list = FileContainer.getlist("studentFilesToUpload")
    StudentFiles = FileContainer["studentFilesToUpload"]
    TemplateFile = FileContainer["templateFileToUpload"]
    user_dir_name_component = request.user.uuid
    print(user_dir_name_component)
    user_dir_path_name = os.path.join(settings.MEDIA_ROOT,str(user_dir_name_component))
    studentfiles_path_name = os.path.join(user_dir_path_name, "studentfiles")
    templatefile_path_name = os.path.join(user_dir_path_name, "templatefile")
    # Check if user directory exists. Create directory if not present
    #print("Files still open from previous run")
    #for proc in psutil.process_iter():
    #    print(proc.open_files())

    for root, dirs, files in os.walk(user_dir_path_name, topdown=False):
        for f in files:
            print("File to delete=", f)
            
        for d in dirs:
            print("Directory to delete=", d)    
    if os.path.exists(user_dir_path_name):
        for filename in os.listdir(user_dir_path_name):
            file_path = os.path.join(user_dir_path_name, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
                progPrint('Failed to delete %s. Reason: %s' % (file_path, e))
                return HttpResponse(status=500)
    else:
        try:
            os.mkdir(user_dir_path_name)
        except OSError:
            print ("Creation of the directory %s failed" % user_dir_path_name)
            progPrint ("Creation of the directory %s failed" % user_dir_path_name)
            return HttpResponse(status=500)
        else:
            print ("Successfully created the directory %s " % user_dir_path_name)           
            

    # Check if studentfiles directory exists. Create directory if not present
    if not os.path.exists(studentfiles_path_name):
        try:
            os.mkdir(studentfiles_path_name)
        except OSError:
            print ("Creation of the directory %s failed" % studentfiles_path_name)
            progPrint ("Creation of the directory %s failed" % studentfiles_path_name)
            return HttpResponse(status=500)
        else:
            print ("Successfully created the directory %s " % studentfiles_path_name)
            

    # Check if templatefile directory exists. Create directory if not present
    if not os.path.exists(templatefile_path_name):
        try:
            os.mkdir(templatefile_path_name)
        except OSError:
            print ("Creation of the directory %s failed" % templatefile_path_name)
            return HttpResponse(status=500)
        else:
            print ("Successfully created the directory %s " % templatefile_path_name)                  

    # upload files into template and student files directories.

    # Template File First.
    filenameoftemplate, file_ext = os.path.splitext(str(TemplateFile))
    print("Uploading file " + str(TemplateFile))
    progPrint("Uploading file " + str(TemplateFile))
    temp_template_file = "templatefile" + file_ext
    with default_storage.open(os.path.join(templatefile_path_name, temp_template_file), 'wb+') as destination:
        for chunk in TemplateFile.chunks():
            destination.write(chunk)

    # Student Files Next
    
    

    x = 0
    for StudentFile in student_files_list:
        filenameofstudent, file_ext = os.path.splitext(str(StudentFile))
        print("Uploading file " + str(StudentFile))
        progPrint("Uploading file " + str(StudentFile))
        temp_student_file = "studentfile" + str(x+1)  + file_ext
        with default_storage.open(os.path.join(studentfiles_path_name, temp_student_file), 'wb+') as destination:
            #for chunk in StudentFile.chunks():
            for chunk in StudentFile.chunks():
                destination.write(chunk)
        x = x + 1    
    
    #for filename, file in request.FILES.iteritems():
    #    name = request.FILES[filename].name
    #    print(name)
    database_User = CustomUser.objects.get(username= request.user.username)
    MainProcessingObject = setupMain(os.path.join(templatefile_path_name, temp_template_file), studentfiles_path_name, request, database_User.mode)
    MainProcessingObject.process()
    return HttpResponse(status = 200)

def login_page(request):
    return render(request, "registration/login.html")

def logout(request):
    return render(request, "mys/home.html")    

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration/registration_form.html', {'form': form})
    #return render(request, "registration/registration_form.html")    

@login_required
def MYS(request):
    return render(request, "mys/MYS.html")

def contact(request):
    return render(request, "mys/contact.html")

def help(request):
    return render(request, "mys/help.html") 




def hello_there(request, name):
    return render(
        request,
        'mys/hello_there.html',
        {
            'name': name,
            'date': datetime.now()
        }
    )

def log_message(request):
    form = LogMessageForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            message = form.save(commit=False)
            message.log_date = datetime.now()
            message.save()
            return redirect("home")
    else:
        return render(request, "mys/log_message.html", {"form": form})

@login_required
def download_results(request):
    user_dir_path_name = os.path.join(settings.MEDIA_ROOT,str(request.user.uuid))
    filename = os.path.join(user_dir_path_name , "results.zip")
    #filename = 'whatever_in_absolute_path__or_not.pdf'
    #content = FileWrapper(filename)
    #content = open(filename, 'r')
    progPrint("***DISABLE_BUTTON***")
    response = HttpResponse(open(filename, 'rb'), content_type='application/force-download')
    response['Content-Length'] = os.path.getsize(filename)
    response['Content-Disposition'] = 'attachment; filename=%s' % 'results.zip'
    return response