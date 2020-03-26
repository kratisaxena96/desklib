from django.conf import settings
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone

from desklib.utils import get_client_ip
from subscription.utils import get_current_subscription


class SubscriptionCheckMixin(object):
    def dispatch(self, request, *args, **kwargs):
        subscription = get_current_subscription(self.request.user)

        if subscription:
            return super(SubscriptionCheckMixin, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('subscription'))
