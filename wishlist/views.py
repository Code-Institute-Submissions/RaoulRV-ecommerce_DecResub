from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from products.models import Carlist
from .models import Wishlist

# Create your views here.


@login_required
def wishlist_view(request):
    wishlist_cars_number = 0

    try:
        all_wishlist = Wishlist.objects.filter(user_name=request.user.id)[0]
    except IndexError:
        wishlist_cars = None
    else:
        wishlist_cars = all_wishlist.products.all()
        wishlist_cars_number = all_wishlist.products.all().count()

    if not wishlist_cars:
        messages.info(request, 'Your wishlist has no cars in it !')

    template = 'wishlist/wishlist.html'
    context = {
        'wishlist_cars': wishlist_cars,
        'wishlist_cars_number': wishlist_cars_number
    }

    return render(request, template, context)

