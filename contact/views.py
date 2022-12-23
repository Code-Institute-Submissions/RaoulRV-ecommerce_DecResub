from django.shortcuts import render, redirect, reverse, get_object_or_404
from .forms import ContactUsForm
from django.contrib import messages
from .models import ContactUs
from django.http import HttpResponseRedirect


def submit_message(request):
    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Thanks for getting in touch, we'll get back to you ASAP !")
            return redirect(reverse('contact'))

        else:
            messages.error(
                request, "There was an error when sending your message.")

    else:
        form = ContactUsForm()

    template = 'contact/contact.html'

    return render(request, template, {'form': form})
