from django.template.response import TemplateResponse

def poster_garden_pro(request):
    return TemplateResponse(request, "poster/garden_pro.html")