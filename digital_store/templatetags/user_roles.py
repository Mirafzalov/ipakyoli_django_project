from django import template

register = template.Library()


@register.filter()
def is_buyer(user):
    return hasattr(user, 'buyer_profile')


@register.filter()
def is_seller(user):
    return hasattr(user, 'seller_profile')