from django.template.response import TemplateResponse

def blog(request): 
    return TemplateResponse(request, "blog/index.html", {})