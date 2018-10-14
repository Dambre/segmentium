# from django.shortcuts import render
import datetime

from django.http import JsonResponse
from django.db.models import Count, Avg

from django.contrib.postgres.aggregates.general import ArrayAgg

from collections import defaultdict
from .models import Order, Customer


def impulse_customers(request):
    stats = {}
    return JsonResponse(stats)


def rare_products_buying_customers(request):
    stats = {}
    return JsonResponse(stats)


def frequent_past_customers(request):
    stats = {}
    return JsonResponse(stats)


def x_y_customers(request):
    stats = {}
    return JsonResponse(stats)


def die_hard_customers(request):
    stats = {}
    return JsonResponse(stats)


def loyal_customers(request):
    orders_count = Order.objects.count()
    customers = Order.objects.all()\
        .values('customer')\
        .annotate(total=Count('customer'))\
        .annotate(orders=ArrayAgg('created_at'))\
        .filter(total__gt=10)
    all_average_timedeltas = []
    for customer in customers:
        orders = sorted(customer['orders'], reverse=True)
        timedeltas = [orders[i - 1] - orders[i] for i in range(1, len(orders))]
        customer_average = average_timedelta(timedeltas)
        customer.update({'average_between_orders': customer_average})
        all_average_timedeltas.append(customer_average)

    customers = sorted(customers, key=lambda x: x['average_between_orders'], reverse=True)[int(len(customers) * 0.2):int(len(customers) * 0.5)]
    stats = {
        'tag': 'loyal_customers',
        'amount': sum([c['total'] for c in customers]),
        'total': orders_count,
        'customers': [c['customer'] for c in customers]
    }
    return JsonResponse(stats)


def at_risk_repeat_customers(request):
    orders_count = Order.objects.count()
    customers = Order.objects.all()\
        .values('customer')\
        .annotate(total=Count('customer'))\
        .annotate(orders=ArrayAgg('created_at'))\
        .filter(total__gt=1)
    all_average_timedeltas = []
    for customer in customers:
        orders = sorted(customer['orders'], reverse=True)
        timedeltas = [orders[i - 1] - orders[i] for i in range(1, len(orders))]
        customer_average = average_timedelta(timedeltas)
        customer.update({'average_between_orders': customer_average})
        all_average_timedeltas.append(customer_average)

    total_average = average_timedelta(all_average_timedeltas)
    customers = [c for c in customers if c['average_between_orders'] < total_average]
    stats = {
        'tips': "Make sure they don't leave you! Send them coupon codes, 'We miss you' emails, win-back surveys",
        'tag': 'at_risk_repeat_customers',
        'amount': sum([c['total'] for c in customers]),
        'total': orders_count,
        'customers': [c['customer'] for c in customers]
    }
    return JsonResponse(stats)


def average_timedelta(timedeltas):
    return sum(timedeltas, datetime.timedelta(0)) / len(timedeltas)


def repeat_customers(request):
    orders_count = Order.objects.count()
    customers = Order.objects.all()\
        .values('customer')\
        .annotate(total=Count('customer'))\
        .filter(total__gt=1)

    stats = {
        'tips': 'Send them refer-a-friend prompts, complementary product recommendations, product review requests',
        'tag': 'repeat_customers',
        'amount': sum([c['total'] for c in customers]),
        'total': orders_count,
        'customers': [c['customer'] for c in customers]
    }
    return JsonResponse(stats)


def one_time_customers(request):
    orders_count = Order.objects.count()
    customers = Order.objects.all()\
        .values('customer')\
        .annotate(total=Count('customer'))\
        .filter(total=1)

    stats = {
        'tips': 'Send them related products, product discounts, product review requests',
        'tag': 'one_time_customers',
        'amount': sum([c['total'] for c in customers]),
        'total': orders_count,
        'customers': [c['customer'] for c in customers]
    }
    return JsonResponse(stats)


def most_frequent_buyers(request):
    customers_count = Customer.objects.count()
    orders_count = Order.objects.count()
    customers = Order.objects.all()\
        .values('customer')\
        .annotate(total=Count('customer'))\
        .order_by('-total')[:int(customers_count / 10)]
    stats = {
        'tag': 'most_frequent_buyers',
        'amount': sum([c['total'] for c in customers]),
        'total': orders_count,
        'customers': [c['customer'] for c in customers]
    }
    return JsonResponse(stats, safe=False)


def customers(request):
    customers = Customer.objects.all()
    return JsonResponse([c.id for c in customers], safe=False)


def most_used_tags(request):
    orders = Order.objects.select_related('product').all()
    total = Order.objects.count()
    return JsonResponse(calculate_order_statistics(orders, total), safe=False)


def calculate_order_statistics(orders, total):
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

    return tags_dict_to_list(used_tags, total)


def tags_dict_to_list(tags, total):
    return sorted([{
        'tag': k,
        'amount': v['amount'],
        'customers': v['customers'],
    } for k, v in tags.items()], key=lambda x: x['amount'], reverse=True)
