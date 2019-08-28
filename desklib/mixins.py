import socket

from django.http import Http404
from desklib.settings.dev_settings import ALLOWED_IPS
from desklib.utils import get_client_ip


class RestrictIpMixin(object):
    def dispatch(self, request, *args, **kwargs):
        ipAddr = get_client_ip(request)
        if ipAddr in ALLOWED_IPS:
            return super(RestrictIpMixin, self).dispatch(request, *args, **kwargs)
        else:
            raise Http404
