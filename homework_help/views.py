from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView, FormView, ListView
from homework_help.models import Order, Comment
from homework_help.forms import CommentForm

# Create your views here.


class OrderDetailView(LoginRequiredMixin, FormView):
    model = Order
    template_name = 'homework_help/order_detail.html'
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        order = Order.objects.get(order_id=self.kwargs['order_id'])
        context['order'] = order
        return context

