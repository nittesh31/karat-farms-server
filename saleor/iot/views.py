from django.template.response import TemplateResponse


def onoff(request):
    return TemplateResponse(request, "iot/onoff.html", {})
