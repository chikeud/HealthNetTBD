from django.contrib import admin
from .models import *

admin.site.register(Hospital)
admin.site.register(Record)
admin.site.register(Prescription)
admin.site.register(Test)