from django.shortcuts import render
from django.views.generic import TemplateView
from homework_help.models import Order

# Create your views here.


class OrderDetailView(TemplateView):
    model = Order
    template_name = 'homework_help/order_detail.html'
