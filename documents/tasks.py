import datetime
import json
import requests
from django.utils import timezone

from celery.schedules import crontab
from celery.task import periodic_task
from django.core.management import call_command
from django.conf import settings


@periodic_task(run_every=(crontab(minute=1, hour=0)), name="index_documents", ignore_result=True)
def index_documents():
    publishdate = timezone.now()-datetime.timedelta(days=1)
    call_command('update_index', start=str(publishdate))


@periodic_task(run_every=(crontab(minute=0, hour='*/7')), name="paypal_auth_token", ignore_result=True)
def paypal_auth_token():
    url = settings.PAYPAL_TOKEN_API

    data = {
        "grant_type": "client_credentials"
    }
    headers = {
        'content-type': "application/x-www-form-urlencoded",
    }
    client = settings.PAYPAL_CLIENT
    secret = settings.PAYPAL_SECRET

    auth = (client, secret)

    resp = requests.request("POST", url, data=data, headers=headers, auth=auth)
    auth_token = json.loads(resp.text).get('access_token')
    f = open(settings.BASE_DIR + "/authtoken.txt", "w")
    f.write(auth_token)
    f.close()

