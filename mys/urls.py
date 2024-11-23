from django.urls import path
from mys import views
from mys.models import LogMessage
from django.conf.urls import include

home_list_view = views.HomeListView.as_view(
    queryset=LogMessage.objects.order_by("-log_date")[:5],  # :5 limits the results to the five most recent
    context_object_name="message_list",
    template_name="mys/home.html",
)

urlpatterns = [
    path("", home_list_view, name="home"),
    path("hello/<name>", views.hello_there, name="hello_there"),
    path("about/", views.about, name="about"),
    path("help/",views.help, name="help"),
    path("contact/", views.contact, name="contact"),
    path("MYSApp/", views.MYS, name="MYS App"),
    path("log/", views.log_message, name="log"),
    path("MYSApp/FileUpload/", views.FileUpload, name="File_Upload"),
    path("MYSApp/ProcessOptionChange/", views.ProcessOptionChange, name="Process_Options_Change"),
    path('accounts/', include('django.contrib.auth.urls')),
    path("accounts/login/", views.login_page, name="login"),
    path("accounts/register/", views.register, name="register"),
    
]

