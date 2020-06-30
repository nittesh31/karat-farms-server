from django.conf.urls import url

from . import views

urlpatterns = [
    url(r"^iot-test-on-off/$", views.iotDashboard, name="dashboard"),
    url(r"^change-timer/$", views.changetimer, name="changetimer"),
    url(r"^on/$", views.on, name="on"),
    url(r"^off/$", views.off, name="off"),

]
