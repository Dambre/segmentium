# from django.shortcuts import render
from django.http import JsonResponse
from collections import defaultdict
from .models import Order


def most_used_tags(request):
    orders = Order.objects.select_related('product').all()
    used_tags = defaultdict(dict)
    for order in orders:
        for tag in order.product.tags:
            try:
                used_tags[tag]['amount'] += 1
            except KeyError:
                used_tags[tag]['amount'] = 1
            try:
                used_tags[tag]['customers'].append(order.customer_id)
            except KeyError:
                used_tags[tag]['customers'] = [order.customer_id]

    return JsonResponse(tags_dict_to_list(used_tags), safe=False)


def tags_dict_to_list(tags):
    return sorted([{
        'tag': k,
        'amount': v['amount'],
        'customers': v['customers'],
    } for k, v in tags.items()], key=lambda x: x['amount'], reverse=True)
