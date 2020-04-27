from django.conf.urls import url

from . import views

urlpatterns = [
    url(r"^contact-save/$", views.contact, name="contact")
]
