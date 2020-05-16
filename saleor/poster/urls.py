from django.conf.urls import url

from . import views

urlpatterns = [
    url(r"^poster-garden-pro/$", views.poster_garden_pro, name="poster-garden-pro")
]
