from django.conf import settings
from django.http import Http404
from django.shortcuts import redirect
from django.utils import timezone

from desklib.utils import get_client_ip


class RestrictIpMixin(object):
    def dispatch(self, request, *args, **kwargs):
        ipAddr = get_client_ip(request)
        if ipAddr in settings.ALLOWED_IPS:
            return super(RestrictIpMixin, self).dispatch(request, *args, **kwargs)
        else:
            raise Http404


class CheckSubscriptionMixin(object):
    def dispatch(self, request, *args, **kwargs):

        if self.request.user.subscriptions.all().filter(expire_on__gt=timezone.now()):
            return redirect('already_subscribed')
        else:
            return super(CheckSubscriptionMixin, self).dispatch(request, *args, **kwargs)