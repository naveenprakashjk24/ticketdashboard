# from django.urls import path,include
# from . import views



# urlpatterns = [
#     path('login/', views.loginPage, name='login'),
#     path('register/', views.registerPage, name='register'),
#     path('home/', views.home, name='home'),
    
# ]

from django.urls import path, re_path
from .views import login_view, register_user, index, pages,requestpage,logoutUser, settingpage, deleteStatus, changesPage, deletePriority,deleteService,deleteIncident,deleteTechuser,knowladgePage


urlpatterns = [
    path('login/', login_view, name="login"),
    path('register/', register_user, name="register"),
    path("logout/", logoutUser, name="logout"),
        # The home page
    path('', index, name='home'),
    path('request/', requestpage, name="request"),
    path('setting/', settingpage, name="setting"),
    path('changes/', changesPage, name="changes"),
    path('knowladge/', knowladgePage, name="knowladge"),
    path('delete-priority/<str:pk>', deletePriority, name="delete-priority"),
    path('delete-incident/<str:pk>', deleteIncident, name="delete-incident"),
    path('delete-service/<str:pk>', deleteService, name="delete-service"),
    path('delete-status/<str:pk>', deleteStatus, name="delete-status"),
    path('delete-tuser/<str:pk>', deleteTechuser, name="delete-tuser"),
    
    # Matches any html file
    re_path(r'^.*\.*', pages, name='pages'),
]

