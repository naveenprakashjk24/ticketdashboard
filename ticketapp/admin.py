from django.contrib import admin
from .models import RequestTicket, Incident_Category, Tech_User, Notes, Status, Priority,Service_Category

# Register your models here.

admin.site.register(RequestTicket)
admin.site.register(Incident_Category)
admin.site.register(Tech_User)
admin.site.register(Notes)
admin.site.register(Status)
admin.site.register(Priority)
admin.site.register(Service_Category)