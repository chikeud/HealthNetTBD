from django.conf.urls import url, include
from . import views

app_name = 'accounts'

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^patientregister/$', views.registerPatient, name='patient_register'),
    url(r'^registeremployee/(?P<employee_type>[0-9])/$', views.registerEmploylee, name='register_employee'),
    url(r'^login/$', views.loginUser, name='login'),
    url(r'^logout/$', views.logoutUser, name='logout'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^update/$', views.updateInfo, name='update'),
    url(r'searchpatients/$', views.searchPatient, name='search_patient'),
    url(r'^register/$', views.register, name='register'),
    url(r'^message/$', views.message, name='message'),


]
