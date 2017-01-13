from django.conf.urls import url
from . import views

app_name = 'records'

urlpatterns = [
    url(r'^viewrecord/(?P<user_id>[0-9]+)/$', views.viewPatientRecord, name='view_patient_record'),
    url(r'^updaterecord/(?P<record_id>[0-9]+)/$', views.updateRecord, name='update_record'),

    url(r'^addprescription/(?P<record_id>[0-9]+)/$', views.addPrescription, name='add_prescription'),
    url(r'^prescription/(?P<rx_id>[0-9]+)/$', views.prescriptionDetail, name='prescription_detail'),
    url(r'^editprescription/(?P<rx_id>[0-9]+)/$', views.editPrescription, name='edit_prescription'),
    url(r'^removeprescription/(?P<rx_id>[0-9]+)/$', views.removePrescription, name='remove_prescription'),

    url(r'^addtest/(?P<record_id>[0-9]+)/$', views.addTest, name='add_test'),
    url(r'^test/(?P<test_id>[0-9]+)/$', views.testDetail, name='test_detail'),
    url(r'^edittest/(?P<test_id>[0-9]+)/$', views.editTest, name='edit_test'),
    url(r'^removetest/(?P<test_id>[0-9]+)/$', views.removeTest, name='remove_test'),

    url(r'^admitpatient/(?P<record_id>[0-9]+)/$', views.admitPatient, name='admit_patient'),
    url(r'^dischargepatient/(?P<record_id>[0-9]+)/$', views.dischargePatient, name='discharge_patient'),
]