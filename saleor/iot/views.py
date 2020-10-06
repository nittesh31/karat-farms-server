from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from .forms import ChangeTimerForm
from .models import FarmImage
import requests
import boto3
import base64

from django.http import HttpResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
import io
import datetime
from concurrent.futures import ThreadPoolExecutor

s3_client = boto3.client('s3',
                         aws_access_key_id='AKIAJMONY4HMYTLPXIWA',
                         aws_secret_access_key='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')

@login_required
def iotDashboard(request):
    form = ChangeTimerForm()
    all_images = []
    for i in range(5):
        objects = FarmImage.objects.filter(email=request.user.email, camera_no=i).order_by('-time_created')[:5]
        images = []
        for object in objects:
            try:
                response = s3_client.get_object(Bucket='karat-video-test', Key=object.image_name)
                images.append(base64.b64encode(response['Body'].read()).decode('utf-8'))
            except s3_client.exceptions.NoSuchKey :
                print("No key found for image")
        if len(images) != 0 :
            all_images.append(images)
    return TemplateResponse(request, "iot/onoff.html", {"user": request.user, "form": form, "all_images" : all_images})


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

def byte_array_to_pil_image(byte_array):
    return Image.open(io.BytesIO(byte_array))

def upload_image(payload, user_email, camera_no):
    img = byte_array_to_pil_image(payload)
    in_mem_file = io.BytesIO()
    img.save(in_mem_file, 'jpeg')
    in_mem_file.seek(0)
    imgName = user_email + "-" + str(datetime.datetime.now()) + "-" + str(camera_no) + ".jpg"
    s3_client.upload_fileobj(in_mem_file, "karat-video-test", imgName)
    FarmImage(email=user_email, image_name=imgName, camera_no=camera_no).save()


executor = ThreadPoolExecutor(max_workers=2)

@csrf_exempt
def post_image(request):
    if request.method == 'POST':
       user_email = request.GET.get('email')
       camera_no = int(request.GET.get('camera_no', 0))
       executor.submit(upload_image, request.body, user_email, camera_no)
       return HttpResponse("hi-post")

@csrf_exempt
def get_new_bin(request):
    return FileResponse(open("./karat-farms-iot.ino.esp32.bin", "rb"))
