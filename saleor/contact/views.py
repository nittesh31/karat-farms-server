from .forms import ContactForm
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import messages
from .models import Contact


def contact(request):
    form_class = ContactForm

    if request.method == 'POST':
        form = form_class(data=request.POST)
        if form.is_valid():
            print(form.cleaned_data['contact_name'])
            print(form.cleaned_data['contact_phone'])

            contact = Contact(
                name=form.cleaned_data['contact_name'],
                phone=form.cleaned_data['contact_phone']
            )
            contact.save()

            messages.success(request, 'Thanks for contacting us. We will get in touch with you soon.')
            return redirect('/#contact')