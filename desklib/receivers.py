from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received, invalid_ipn_received
from subscription.models import Subscription, Plan
from accounts.models import UserAccount
from datetime import timedelta
from django.template.loader import render_to_string
from post_office import mail
from django.conf import settings



def show_me_the_money(sender, **kwargs):
    ipn_obj = sender

    if ipn_obj.payment_status == ST_PP_COMPLETED:
        # WARNING !
        # Check that the receiver email is the same we previously
        # set on the `business` field. (The user could tamper with
        # that fields on the payment form before it goes to PayPal)
        if ipn_obj.receiver_email == "info-facilitator@a2zservices.net":
            if ipn_obj.txn_id:
                custom_str = ipn_obj.custom
                custom_str_list = custom_str.split('_')
                username = custom_str_list[0]
                plan_key = custom_str_list[1]
                plan = Plan.objects.get(key=plan_key)
                plan_days = plan.days
                payment_date = ipn_obj.payment_date
                expire_on = payment_date + timedelta(days=plan_days)
                user = UserAccount.objects.get(username=username)
                try:
                    contex={'traction_id':ipn_obj.txn_id,'currency':ipn_obj.mc_currency,'amount':ipn_obj.payment_gross,'payment_date':payment_date,'expiry':expire_on,'plan':plan.package_name}
                    htmly = render_to_string('desklib/mail-templates/payment_success_email_template.html',context=contex,request=None)
                    mail.send(
                        user.email,
                        settings.DEFAULT_FROM_EMAIL,
                        subject='Payment Success Confirmation From Desklib',
                        # message=htmly,
                        html_message=htmly,
                        # attachments=attachments,
                        priority='now'
                    )

                except Exception as e:
                    print("Payment Success Email Sending failed",e)
                subscription =  Subscription.objects.create(user=user, plan=plan, expire_on=expire_on, author=user)
        else:
            return

    else:
        print("Payment Failed")

valid_ipn_received.connect(show_me_the_money)


def invalid_payment(sender, **kwargs):
    ipn_obj = sender
    print("Invalid Payment done")



invalid_ipn_received.connect(invalid_payment)