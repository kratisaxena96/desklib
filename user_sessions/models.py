from django.db import models
from django.conf import settings
from django.contrib.sessions.models import Session
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib.gis.geoip2 import GeoIP2


# https://stackoverflow.com/questions/235950/how-to-lookup-django-session-for-a-particular-user/6238346
# http://gavinballard.com/associating-django-users-sessions/
class UserSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    session = models.OneToOneField(Session, on_delete=models.CASCADE)
    user_agent = models.CharField(null=True, blank=True, max_length=250)
    # last_activity = models.DateTimeField(auto_now=True)

    ip = models.GenericIPAddressField(null=True, blank=True, verbose_name='IP')
    created = models.DateTimeField(editable=False)
    last_activity = models.DateTimeField()
    city = {}
    country = {}

    class Meta:
        verbose_name = _('user session')
        verbose_name_plural = _('user sessions')

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        self.last_activity = timezone.now()
        g = GeoIP2()
        try:
            self.country = g.country(self.ip)
        except:
            self.country = {'country_name':'unidentify'}

        return super(UserSession, self).save(*args, **kwargs)


def user_logged_in_handler(sender, request, user, **kwargs):

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    ip_addr = ""
    if x_forwarded_for:
        ip_addr = x_forwarded_for.split(',')[0]
    else:
        ip_addr = request.META.get('REMOTE_ADDR')

    user, created = UserSession.objects.get_or_create(
        user = user,
        session_id = request.session.session_key,
        ip=ip_addr,
        user_agent=request.META.get('HTTP_USER_AGENT', ''),
    )
    if not created:
        # Update last activity time for session
        user.save()


user_logged_in.connect(user_logged_in_handler)

def user_logged_out(sender, user, request, **kwargs):
    session_logout = UserSession.objects.filter(session_id=request.session.session_key)
    session_logout.delete()
