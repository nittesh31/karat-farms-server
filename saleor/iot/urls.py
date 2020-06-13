from django.conf.urls import url

from . import views

urlpatterns = [
    url(r"^iot-test-on-off/$", views.onoff, name="onoff")
]
