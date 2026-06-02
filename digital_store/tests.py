from django.core.paginator import Paginator
from django.http import JsonResponse

from digital_store.models import Order


def get_order(request):
    page = int(request.GET.get('page', 1))
    orders = Order.objects.all().order_by('-id')
    paginator = Paginator(orders, 3)
    page_obj = paginator.get_page(page)
    products = ''
    data = []
    for order in page_obj:
        # for p in order.products_order:
        #     products += {p.title}
        data.append({
            'id': order.id,
            'user': order.user.first_name,
            'phone': order.user.username,
            # 'products': products,
            'price': order.price,
            'created_at': order.created_at.strftime("%Y-%m-%d %H:%M")
        })

    context = {
        'orders': data,
        'page': page_obj.number,
        'total': page_obj.paginator.num_pages,
        'has_previous': page_obj.has_previous(),
        'has_next': page_obj.has_next(),
        'previous_page': page_obj.previous_page_number() if page_obj.has_previous() else None,
        'next_page': page_obj.next_page_number() if page_obj.has_next() else None
    }

    return JsonResponse(context, safe=True)


