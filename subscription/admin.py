from django.contrib import admin
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from subscription.models import Plan, Subscription, Download, PageView, SessionPageView, PayPerDocument


# Register your models here.




def pay_per_subs_mail(modeladmin, request, queryset):
    for query in queryset:
        plan = query.plan
        plan_days = plan.days
        # payment_date = ipn_obj.payment_date
        expire_on = query.expire_on
        user = query.user
        site_url = Site.objects.get_current().domain
        docs = query.documents.all()
        doc_slug = []
        for doc in docs:
            doc_slug.append(doc.slug)

        contex = {'expiry': expire_on, 'plan': plan.package_name, 'document_redirect': doc_slug[0], 'SITE_URL': site_url, }
        # pay_doc = PayPerDocument.objects.filter(user=user, start_date=payment_date,documents=doc, expire_on=expire_on)
        # if pay_doc :
        #     pay_doc.documents.add(doc)

        try:
            htmly = render_to_string('desklib/mail-templates/pay_per_subs_for_upload_email_template.html',
                                     context=contex, request=None)
            html_message = htmly
            mail = EmailMultiAlternatives(
                subject='Payment Success Confirmation From Desklib',
                to=[user.email],
                body=''
            )
            # mail = EmailMultiAlternatives(subject, message, from_email, recipient_list)
            mail.attach_alternative(html_message, 'text/html')
            mail.send(True)
        except Exception as e:
            print("Payment Success Email Sending failed", e)


pay_per_subs_mail.short_description = 'Send subscription mail'


class DownloadAdmin(admin.ModelAdmin):
    raw_id_fields = ('document','user')
    search_fields = ['document__title', ]
    list_display = ('document', 'user', 'created_at', 'updated_at')


class PlanAdmin(admin.ModelAdmin):
    raw_id_fields = ('author',)
    search_fields = ['package_name']
    list_display = ('package_name', 'download_limit', 'view_limit', 'author', 'created_at', 'updated_at')


class SubscriptionAdmin(admin.ModelAdmin):
    raw_id_fields = ('user','plan','author','documents')
    search_fields = ['plan__package_name']
    list_display = ('user', 'plan', 'is_current', 'expire_on', 'author', 'created_at', 'updated_at')


class PageViewsAdmin(admin.ModelAdmin):
    raw_id_fields = ('document', 'user')
    search_fields = ['document__title', ]
    list_display = ('document', 'user', 'created_at', 'updated_at')


class SessionPageViewsAdmin(admin.ModelAdmin):
    raw_id_fields = ('document',)
    search_fields = ['document__title', ]
    list_display = ('document', 'session', 'created_at', 'updated_at')

class PayPerViewAdmin(admin.ModelAdmin):
    raw_id_fields = ('documents','user')
    list_display = ('user','is_current')
    actions = [pay_per_subs_mail,]

admin.site.register(PayPerDocument, PayPerViewAdmin)
admin.site.register(Plan,PlanAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(Download, DownloadAdmin)
admin.site.register(PageView, PageViewsAdmin)
admin.site.register(SessionPageView, SessionPageViewsAdmin)


