from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from accounts.utils import *
from .models import *


@login_required()
def viewDailyLogs(request):
    context = RequestContext(request)
    type = get_user_type(request.user)

    if type != "Admin":
        return HttpResponseRedirect(reverse('accounts:home'))

    admin = Admin.objects.get(User__id=request.user.id)
    hospital = admin.Hospital

    logs = DailyLog.objects.filter(Hospital=hospital)
    logs = logs.order_by('-Date')
    return render_to_response(
        'logger/view_daily_logs.html', {'logs': logs}, context)

@login_required()
def viewActivities(request, log_id):
    context = RequestContext(request)
    type = get_user_type(request.user)

    if type != "Admin":
        return HttpResponseRedirect(reverse('accounts:home'))

    log = get_object_or_404(DailyLog, id=int(log_id))
    activities = log.Activities.all()
    activities = activities.order_by('-Date')
    return render_to_response(
        'logger/view_activities.html', {'activities': activities}, context)


@login_required()
def activityDetail(request, activity_id):
    context = RequestContext(request)
    type = get_user_type(request.user)

    if type != "Admin":
        return HttpResponseRedirect(reverse('accounts:home'))

    activity = get_object_or_404(Activity, id=int(activity_id))
    return render_to_response(
        'logger/activity_detail.html', {'activity': activity}, context)