from django.shortcuts import render
from .forms import ContactUsForm
from django.contrib import messages
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
            return redirect(reverse('contact'))
    else:
        form = ContactUsForm()

    template = 'contact/contact.html'

    return render(request, template, {'form': form})
