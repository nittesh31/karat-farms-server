from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from .forms import ChangeTimerForm

import requests


@login_required
def iotDashboard(request):
    form = ChangeTimerForm()
    return TemplateResponse(request, "iot/onoff.html", {"user": request.user, "form": form})



@login_required
def on(request):
    r = requests.post(
        'https://bosc5t1qv3.execute-api.us-west-2.amazonaws.com/Prod/publish',
        json={
            "user": str(request.user),
            "message": "ON"
        }

    )
    return HttpResponseRedirect('/iot-test-on-off/')


@login_required
def off(request):
    r = requests.post(
        'https://bosc5t1qv3.execute-api.us-west-2.amazonaws.com/Prod/publish',
        json={
            "user": str(request.user),
            "message": "OFF"
        }

    )
    return HttpResponseRedirect('/iot-test-on-off/')


@login_required
def changetimer(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ChangeTimerForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            r = requests.post(
                'https://bosc5t1qv3.execute-api.us-west-2.amazonaws.com/Prod/publish',
                json={
                    "user": str(request.user),
                    "message": {
                        'task': 'change_timer',
                        'sl_no': form.cleaned_data['sl_no'],
                        'start_time': form.cleaned_data['start_time'],
                        'duration': form.cleaned_data['duration'],
                        'status': form.cleaned_data['status']
                    }
                }

            )
            return HttpResponseRedirect('/iot-test-on-off/')
