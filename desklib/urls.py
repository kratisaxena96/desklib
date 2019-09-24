"""desklib URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.conf.urls.i18n import i18n_patterns
from .sitemaps import DocumentSitemap, StaticViewSitemap, SampleSitemap
from django.views.decorators.cache import cache_page
from django.contrib.sitemaps import views
from .views import HomePageView, AboutPageView, PricingPageView, ContactPageView, TestPageView, \
    SubscriptionView, PayNowView, PrivacyPolicyView, HonorCodeView, CopyrightPolicyView, TermsOfUseView, \
    AcademicIntegrityView, ComingSoonPageView, PaymentCancelledView, PaymentSuccessView, AlreadySubscribedView
from subscription.views import MyDownloads
# if settings.DEBUG:
#     import debug_toolbar

sitemaps = {
    'documents': DocumentSitemap,
    'static':StaticViewSitemap,
    'samples': SampleSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('accounts/', include('accounts.urls')),  # new
    path('accounts/', include('accounts.urls')),
    path('study/',include(('study.urls','study'),namespace="study")),
    path('', HomePageView.as_view(), name='home'),
    path('coming-soon/', ComingSoonPageView.as_view(), name='coming-soon'),
    path('document/', include(('documents.urls','documents'),namespace="documents")),
    path('my-downloads/', MyDownloads.as_view(),name="my-downloads"),
    path('about/', AboutPageView.as_view(), name='about'),
    path('privacy-policy/', PrivacyPolicyView.as_view(), name='privacypolicy'),
    path('copyright/', CopyrightPolicyView.as_view(), name='copyright'),
    path('honor-code/', HonorCodeView.as_view(), name='honorcode'),
    path('terms-of-use/', TermsOfUseView.as_view(), name='termsofuse'),
    path('academic-integrity/', AcademicIntegrityView.as_view(), name='academicintegrity'),
    path('contact/', ContactPageView.as_view(), name='contact'),
    path('pricing/', PricingPageView.as_view(), name='pricing'),
    path('test/', TestPageView.as_view(), name='test'),
    path('writing/', include(('writing.urls', 'writing'), namespace="writing")),
    path('robots.txt', include('robots.urls')),
    path('sitemap.xml', cache_page(60)(views.index), {'sitemaps': sitemaps}, name='cached-sitemap'),
    path('sitemap-<section>.xml', views.sitemap, {'sitemaps': sitemaps},
                       name='django.contrib.sitemaps.views.sitemap'),
    # path('payment/doc', PaypalPaymentView.as_view(), name='paypal_view'),
    path('subscription/', SubscriptionView.as_view(), name='subscription'),
    path('paynow/<str:key>', PayNowView.as_view(), name='paynow'),
    path('paypal/', include('paypal.standard.ipn.urls'), name='paypal-ipn'),
    path('payment/cancelled', PaymentCancelledView.as_view(), name='payment_cancelled'),
    path('payment/success', PaymentSuccessView.as_view(), name='payment_success'),
    path('subscribed/', AlreadySubscribedView.as_view(), name='already_subscribed'),

    path('api-auth/', include('rest_framework.urls')),
    # path('payment/document',)
    path('api/', include(('api.urls', 'api'), namespace="api")),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += i18n_patterns(
    url(r'^$', HomePageView.as_view(), name='home'),
    # url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]

handler404 = 'desklib.views.handler404'
handler500 = 'desklib.views.handler500'