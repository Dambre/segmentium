from django.urls import path


from . import views

urlpatterns = [
    path('most-used-tags', views.most_used_tags),
]
