from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from .forms import ChangeTimerForm
from .models import FarmImage
import requests
import boto3
import base64
s3_client = boto3.client('s3',
                         aws_access_key_id='AKIAJMONY4HMYTLPXIWA',
                         aws_secret_access_key='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')

@login_required
def iotDashboard(request):
    form = ChangeTimerForm()
    print(request.user.email)
    objects = FarmImage.objects.filter(email=request.user.email).order_by('-time_created')[:5]
    images = []
    for object in objects:
        response = s3_client.get_object(Bucket='karat-video-test', Key=object.image_name)
        images.append(base64.b64encode(response['Body'].read()).decode('utf-8'))
    print(images)
    return TemplateResponse(request, "iot/onoff.html", {"user": request.user, "form": form, "images" : images})


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
