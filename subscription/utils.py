from subscription.models import Subscription
from datetime import timedelta
from datetime import datetime
import pytz
from django.utils import timezone
utc=pytz.UTC

def is_subscribed(user):
    is_subscribed = False

    subscription_qs = user.subscriptions.all()
    for subscription_obj in subscription_qs:
        expiry_subscription_date = subscription_obj.expire_on
        now = timezone.now()

        if expiry_subscription_date > now:
            is_subscribed = True

            return is_subscribed
        else:
            is_subscribed = False

    return is_subscribed

def get_current_subscription(user):
    subscribed_status = is_subscribed(user)

    if subscribed_status:
        subscription_qs = user.subscriptions.all()
        for subscription_obj in subscription_qs:
            expiry_subscription_date = subscription_obj.expire_on
            now = timezone.now()

            if expiry_subscription_date > now:
                return subscription_obj


    else:
        return None
