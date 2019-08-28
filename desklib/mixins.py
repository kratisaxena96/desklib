from django.conf import settings
from django.http import Http404
from desklib.utils import get_client_ip


class RestrictIpMixin(object):
    def dispatch(self, request, *args, **kwargs):
        ipAddr = get_client_ip(request)
        if ipAddr in settings.ALLOWED_IPS:
            return super(RestrictIpMixin, self).dispatch(request, *args, **kwargs)
        else:
            raise Http404
