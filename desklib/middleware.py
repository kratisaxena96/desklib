from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse

from desklib.utils import get_client_ip


class IpRestrict:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        if not request.path == '/coming-soon/':
            ipAddr = get_client_ip(request)
            if settings.COMING_SOON:
                if ipAddr in settings.ALLOWED_IPS:

                    response = self.get_response(request)

                    # Code to be executed for each request/response after
                    # the view is called.

                    return response
                else:
                    # print('coming soon')
                    return HttpResponseRedirect(reverse('coming-soon'))
            else:

                response = self.get_response(request)

                # Code to be executed for each request/response after
                # the view is called.

                return response
        else:

            response = self.get_response(request)

            # Code to be executed for each request/response after
            # the view is called.

            return response
