from django import template


register = template.Library()


@register.filter(name="calc_subtotal")
def calc_subtotal(priceperday, quantity):
    return priceperday * quantity
