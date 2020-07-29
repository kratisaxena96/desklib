from django.conf import settings
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from documents.models import Document
from subscription.models import PayPerDocument

from desklib.utils import get_client_ip
from subscription.utils import get_current_subscription


class SubscriptionCheckMixin(object):
    def dispatch(self, request, *args, **kwargs):
        subscription = get_current_subscription(self.request.user)
        doc = Document.objects.get(slug=request.GET.get('doc'))
        try:
            pay_per_doc = PayPerDocument.objects.get(documents=doc)
        except:
            pay_per_doc = None

        if subscription or pay_per_doc:
            return super(SubscriptionCheckMixin, self).dispatch(request, *args, **kwargs)
        else:

            # url = reverse('blog')
            # number = request
            # return HttpResponseRedirect(url + "?page=%s" % number)
            return HttpResponseRedirect(reverse('documents:document-pay')+ "?doc=" + request.GET.get('doc'))
