from django.db import models
from django.conf import settings
from django.contrib.sessions.models import Session
from django.contrib.auth.signals import user_logged_in
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class UserSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    user_agent = models.CharField(null=True, blank=True, max_length=200)
    # last_activity = models.DateTimeField(auto_now=True)

    ip = models.GenericIPAddressField(null=True, blank=True, verbose_name='IP')
    created = models.DateTimeField(editable=False)
    last_activity = models.DateTimeField()

    class Meta:
        verbose_name = _('user session')
        verbose_name_plural = _('user sessions')

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        self.last_activity = timezone.now()
        return super(UserSession, self).save(*args, **kwargs)


def user_logged_in_handler(sender, request, user, **kwargs):
    user, created = UserSession.objects.get_or_create(
        user = user,
        session_id = request.session.session_key,
        ip=request.META.get('REMOTE_ADDR', ''),
        user_agent=request.META.get('HTTP_USER_AGENT', ''),
    )
    if not created:
        # Update last activity time for session
        user.save()


user_logged_in.connect(user_logged_in_handler)

