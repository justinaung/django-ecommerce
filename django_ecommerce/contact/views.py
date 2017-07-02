from django.contrib import messages
from django.http import HttpRequest
from django.shortcuts import render, redirect

from django_ecommerce.contact.forms import ContactView


def contact(request: HttpRequest):
    if request.method == 'POST':
        form = ContactView(request.POST)
        if form.is_valid():
            our_form = form.save(commit=False)
            our_form.save()
            messages.add_message(request, messages.INFO,
                                 'Your message has been sent. Thank you.')
            return redirect('/')
    else:
        form = ContactView()
    return render(request, 'contact.html', {'form': form})
