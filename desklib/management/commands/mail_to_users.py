from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand
from documents.models import Document
from django.conf import settings
from post_office import mail
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.db.models import Q


class Command(BaseCommand):
    help = 'Command to send mails to Signup Users'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        emails = []
        if settings.FLAG_MAIL_TO_TEST:
            users = User.objects.filter(is_staff=True, is_active=True)
        else:
            users = User.objects.filter(is_active=True, is_staff=False)
        for user in users:
            emails.append(user.email)

        doc = Document.objects.filter(page__gte=8,views__gte=2,is_featured=True,is_visible=True)
        email_doc = {}
        if doc:
            for document in doc:
                try:
                    document.pages.get(no=document.cover_page_number).image_file.url
                    email_doc.__setitem__(document, document.pages.get(no=doc.cover_page_number).image_file.url)
                except:
                    if document.pages.count() >= 2:
                        url = document.pages.all()[1].image_file.url
                        email_doc.__setitem__(document, url)
                    elif document.pages.count() == 1:
                        url = document.pages.first().image_file.url
                        email_doc.__setitem__(document, url)
            context = {'doc': email_doc}

            html_template = render_to_string('desklib/mail-templates/subscription_email_template.html', context)
            subject = 'Weekly Digest from desklib.com'
            message = ''
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [emails],
            html_message = html_template
            mail = EmailMultiAlternatives(subject, message, from_email, recipient_list)
            mail.attach_alternative(html_message, 'text/html')
            mail.send(True)
            # mail.send(
            #     emails,
            #     settings.DEFAULT_FROM_EMAIL,
            #     subject='Weekly Digest from desklib.com',
            #     html_message=html_template,
            #     priority='now'
            # )
