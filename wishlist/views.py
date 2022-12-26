from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from products.models import Carlist
from .models import Wishlist
from django.http import Http404

# Create your views here.


@login_required
def wishlist_view(request):
    wishlist_cars_number = 0

    try:
        all_wishlist = Wishlist.objects.filter(user_name=request.user.id)[0]
    except IndexError:
        wishlist_cars = None
    else:
        wishlist_cars = all_wishlist.wishlist_cars.all()
        wishlist_cars_number = all_wishlist.wishlist_cars.all().count()

    if not wishlist_cars:
        messages.info(request, 'Your wishlist has no cars in it !')

    template = 'wishlist.html'
    context = {
        'wishlist_cars': wishlist_cars,
        'wishlist_cars_number': wishlist_cars_number
    }

    return render(request, template, context)


@login_required
def add_to_wishlist(request, item_id):

    product = get_object_or_404(Carlist, pk=item_id)
    try:
        wishlist = get_object_or_404(Wishlist, user_name=request.user.id)
    except Http404:
        wishlist = Wishlist.objects.create(user_name=request.user)

    if product in wishlist.wishlist_cars.all():
        messages.info(request, 'This car is already in your wishlist !')
        messages.info(request, f'{product.name} is already in your \
            wishlist !')

    else:
        wishlist.wishlist_cars.add(product)
        messages.success(request, f'{product.name} has been added \
            to your wishlist !')

    return redirect(reverse('product_detail', args=[product.id]))


@login_required
def remove_from_wishlist(request, item_id, redirect_from):

    product = get_object_or_404(Carlist, pk=item_id)
    wishlist = get_object_or_404(Wishlist, user_name=request.user.id)
    if product in wishlist.wishlist_cars.all():
        wishlist.wishlist_cars.remove(product)
        messages.success(request, f'{product.name} has been removed \
            from your wishlist !')
    else:
        messages.error(request, f'{product.name} is not in your wishlist !')

    if redirect_from == 'wishlist':
        redirect_url = reverse('wishlist')
    else:
        redirect_url = reverse('product_detail', args=[product.id])

    return redirect(redirect_url)