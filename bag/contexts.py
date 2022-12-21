from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Carlist
from datetime import date, timedelta


def bag_contents(request):

    bag_items = []
    total = 0
    product_count = 0
    bag = request.session.get("bag", {})
    for item_id, item_data in bag.items():
        if isinstance(item_data, int):
            product = get_object_or_404(Carlist, pk=item_id)
            total += item_data * product.priceperday
            product_count += item_data
            bag_items.append(
                {
                    "item_id": item_id,
                    "quantity": item_data,
                    "product": product,
                }
            )
        else:
            product = get_object_or_404(Carlist, pk=item_id)
            for size, quantity in item_data["items_by_size"].items():
                total += quantity * product.priceperday
                product_count += quantity
                bag_items.append(
                    {
                        "item_id": item_id,
                        "quantity": quantity,
                        "product": product,
                    }
                )

    maintenance = total * Decimal(settings.STANDARD_MAINTENANCE_PERCENTAGE / 100)

    grand_total = maintenance + total

    context = {
        "bag_items": bag_items,
        "total": total,
        "product_count": product_count,
        "maintenance": maintenance,
        "grand_total": grand_total,
    }

    return context
