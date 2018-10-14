from django.urls import path


from . import views

urlpatterns = [
    path('most-used-tags', views.most_used_tags),
    path('most-frequent-buyers', views.most_frequent_buyers),
    path('one-time-customers', views.one_time_customers),
    path('repeat-customers', views.repeat_customers),
    path('at-risk-repeat-customers', views.at_risk_repeat_customers),
    path('loyal-customers', views.loyal_customers),
    path('die-hard-customers', views.die_hard_customers),
    path('x-y-customers', views.x_y_customers),
    path('frequent-past-customers', views.frequent_past_customers),
    path('rare-products-buying-customers', views.rare_products_buying_customers),
    path('impulse-customers', views.impulse_customers),
]
