from django.core.mail import EmailMultiAlternatives
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received, invalid_ipn_received
from subscription.models import Subscription, Plan, PayPerDocument
from accounts.models import UserAccount
from datetime import timedelta
from django.template.loader import render_to_string
from homework_help.models import Order
from documents.models import Document
from post_office import mail
from django.conf import settings
from django.conf import settings


def show_me_the_money(sender, **kwargs):
    ipn_obj = sender

    if ipn_obj.payment_status == ST_PP_COMPLETED:
        # WARNING !
        # Check that the receiver email is the same we previously
        # set on the `business` field. (The user could tamper with
        # that fields on the payment form before it goes to PayPal)
        if settings.DEBUG:
            receiver_email = "info-facilitator@a2zservices.net"
            # action="https://www.sandbox.paypal.com/cgi-bin/webscr

            # homework help payment logic
        else:
            receiver_email = "info@a2zservices.net"
        if ipn_obj.receiver_email == receiver_email:
            if ipn_obj.txn_id:

                custom_list = ipn_obj.custom.split('_')
                if custom_list[0] == "homework-help":
                    question = custom_list[1]
                    order = custom_list[2]
                    o = Order.objects.get(uuid=order)
                    o.amount_paid = o.amount_paid + ipn_obj.payment_gross
                    o.status = 3
                    o.save()
                else:
                    custom_str = ipn_obj.custom
                    custom_str_list = custom_str.split('_')
                    username = custom_str_list[0]
                    plan_key = custom_str_list[1]
                    try:
                        doc_slug = custom_str_list[2]
                        doc = Document.objects.get(slug=doc_slug)
                    except:
                        pass
                    plan = Plan.objects.get(key=plan_key)
                    plan_days = plan.days
                    payment_date = ipn_obj.payment_date
                    expire_on = payment_date + timedelta(days=plan_days)
                    user = UserAccount.objects.get(username=username)

                    if plan.is_pay_per_download:
                        contex = {'traction_id': ipn_obj.txn_id, 'currency': ipn_obj.mc_currency,
                                  'amount': ipn_obj.payment_gross, 'payment_date': payment_date, 'expiry': expire_on,
                                  'plan': plan.package_name, 'document_redirect': doc_slug, 'SITE_URL': "https://desklib.com",}
                        # pay_doc = PayPerDocument.objects.filter(user=user, start_date=payment_date,documents=doc, expire_on=expire_on)
                        # if pay_doc :
                        #     pay_doc.documents.add(doc)
                        payperdoc = PayPerDocument.objects.create(user=user, plan=plan, expire_on=expire_on,
                                                                  start_date=payment_date, is_current=True)
                        payperdoc.documents.add(doc)
                    else:
                        contex = {'traction_id': ipn_obj.txn_id, 'currency': ipn_obj.mc_currency,
                                  'amount': ipn_obj.payment_gross, 'payment_date': payment_date, 'expiry': expire_on,
                                  'plan': plan.package_name, }
                        subscription = Subscription.objects.create(user=user, plan=plan, expire_on=expire_on,
                                                                   author=user)

                    try:

                        htmly = render_to_string('desklib/mail-templates/payment_success_email_template.html',
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
                        # mail.send(
                        #     user.email,
                        #     settings.DEFAULT_FROM_EMAIL,
                        #     subject='Payment Success Confirmation From Desklib',
                        #     # message=htmly,
                        #     html_message=htmly,
                        #     # attachments=attachments,
                        #     priority='now'
                        # )

                    except Exception as e:
                        print("Payment Success Email Sending failed", e)
                    # if plan.is_pay_per_download:
                    #     # pay_doc = PayPerDocument.objects.filter(user=user, start_date=payment_date,documents=doc, expire_on=expire_on)
                    #     # if pay_doc :
                    #     #     pay_doc.documents.add(doc)
                    #     payperdoc = PayPerDocument.objects.create(user=user, plan=plan, expire_on=expire_on,
                    #                                               start_date=payment_date, is_current=True)
                    #     payperdoc.documents.add(doc)
                    # else:
                    #     subscription = Subscription.objects.create(user=user, plan=plan, expire_on=expire_on,
                    #                                                author=user)
            else:
                return

    else:
        print("Payment Failed")


valid_ipn_received.connect(show_me_the_money)


def invalid_payment(sender, **kwargs):
    ipn_obj = sender
    print("Invalid Payment done")


invalid_ipn_received.connect(invalid_payment)
