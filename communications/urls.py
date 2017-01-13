from django.conf.urls import url, include
from . import views


app_name = 'communications'
#(?P<user_id>[0-9]+)/$
urlpatterns = [

    url(r'^addappointment/$', views.addAppointment, name='add_appointment'),
    url(r'^viewappointments/$', views.viewAppointments, name='view_appointments'),
    url(r'^editappointment/(?P<appointment_id>[0-9]+)/$', views.editAppointment, name='edit_appointment'),
    url(r'^appointmentdatail/(?P<appointment_id>[0-9]+)/$', views.appointmentDetail, name='appointment_detail'),
    url(r'^deleteappointment/(?P<appointment_id>[0-9]+)/$', views.deleteAppointment, name='delete_appointment'),
    url(r'^sendmessage/$', views.sendMessage, name='send_message'),
    url(r'^viewmessages/$', views.viewMessages, name='view_messages'),
    url(r'^viewmessage/(?P<message_id>[0-9]+)/$', views.messageDetail, name='message_detail'),

]