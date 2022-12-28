from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.functions import Lower
from .models import Carlist, Category, Reviewcar
from .forms import ProductForm, CarReviewForm
from datetime import date
from wishlist.models import Wishlist
from django.http import Http404

# Create your views here.


def all_products(request):
    """A view to show all products, including sorting and search queries"""

    products = Carlist.objects.all()
    query = None
    categories = None
    sort = None
    direction = None

    if request.GET:
        if "sort" in request.GET:
            sortkey = request.GET["sort"]
            sort = sortkey
            if sortkey == "name":
                sortkey = "lower_name"
                products = products.annotate(lower_name=Lower("name"))
            if sortkey == "category":
                sortkey = "category__name"
            if "direction" in request.GET:
                direction = request.GET["direction"]
                if direction == "desc":
                    sortkey = f"-{sortkey}"
            products = products.order_by(sortkey)

        if "category" in request.GET:
            categories = request.GET["category"].split(",")
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if "q" in request.GET:
            query = request.GET["q"]
            if not query:
                messages.error(
                    request, "You didn't enter any search criteria!")
                return redirect(reverse("products"))

            queries = Q(name__icontains=query) | Q(
                description__icontains=query)
            products = products.filter(queries)

    current_sorting = f"{sort}_{direction}"

    context = {
        "products": products,
        "search_term": query,
        "current_categories": categories,
        "current_sorting": current_sorting,
    }

    return render(request, "products/products.html", context)


def product_detail(request, product_id):
    """A view to show individual product details"""

    product = get_object_or_404(Carlist, pk=product_id)
    reviews = Reviewcar.objects.filter(
        car_id=product.id, status=True).order_by('-created_at')
    totalreviews = reviews.count()

    try:
        wishlist = get_object_or_404(Wishlist, user_name=request.user.id)
    except Http404:
        is_in_wishlist = False
    else:
        is_in_wishlist = bool(product in wishlist.wishlist_cars.all())

    context = {
        "is_in_wishlist": is_in_wishlist,
        "product": product,
        'reviews': reviews,
        'totalreviews': totalreviews,
    }

    return render(request, "products/product_detail.html", context)


@login_required
def add_product(request):
    """Add a product to the store"""
    if not request.user.is_superuser:
        messages.error(request, "Sorry, only store owners can do that.")
        return redirect(reverse("home"))

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, "Successfully added product!")
            return redirect(reverse("product_detail", args=[product.id]))
        else:
            messages.error(
                request, "Error! Please ensure the form is valid."
            )
    else:
        form = ProductForm()

    template = "products/add_product.html"
    context = {
        "form": form,
    }

    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    """Edit a product in the store"""
    if not request.user.is_superuser:
        messages.error(request, "Sorry, only store owners can do that.")
        return redirect(reverse("home"))

    product = get_object_or_404(Carlist, pk=product_id)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully updated product!")
            return redirect(reverse("product_detail", args=[product.id]))
        else:
            messages.error(
                request, "Error! Please ensure the form is valid."
            )
    else:
        form = ProductForm(instance=product)
        messages.info(request, f"You are editing {product.name}")

    template = "products/edit_product.html"
    context = {
        "form": form,
        "product": product,
    }

    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    """Delete a product from the store"""
    if not request.user.is_superuser:
        messages.error(request, "Sorry, only store owners can do that.")
        return redirect(reverse("home"))

    product = get_object_or_404(Carlist, pk=product_id)
    product.delete()
    messages.success(request, "Product deleted!")
    return redirect(reverse("products"))


def submit_review(request, product_id):
    product = get_object_or_404(Carlist, pk=product_id)
    if request.method == 'POST':
        form = CarReviewForm(request.POST)
        if form.is_valid():
            data = Reviewcar()
            data.stars = form.cleaned_data['stars']
            data.reviewtitle = form.cleaned_data['reviewtitle']
            data.reviewtext = form.cleaned_data['reviewtext']
            data.car = product
            data.user_id = request.user.id
            data.save()
            messages.success(
                request, 'Your review was successfully submitted!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(
                request, "There was an error when submitting this review!")
            return redirect(reverse('product_detail', args=[product.id]))

    else:
        form = CarReviewForm()

    template = 'products/product_detail.html'

    return render(request, template)


@login_required
def remove_review(request, reviewcar_id):

    review = get_object_or_404(Reviewcar, pk=reviewcar_id)
    product = review.car

    review.delete()
    messages.success(request, 'You have successfully removed the review!')

    return redirect(reverse('product_detail', args=[product.id]))
