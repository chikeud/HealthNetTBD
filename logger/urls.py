from django.conf.urls import url
from . import views

app_name = 'logger'

urlpatterns = [
    url(r'^viewlogs/$', views.viewDailyLogs, name='view_daily_logs'),
    url(r'^viewactivities/(?P<log_id>[0-9]+)/$', views.viewActivities, name='view_activities'),
    url(r'^activitydetail/(?P<activity_id>[0-9]+)/$', views.activityDetail, name='activity_detail')
]