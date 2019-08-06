from django.apps import AppConfig


class DesklibConfig(AppConfig):
    name = 'desklib'

    def ready(self):
        # import signal handlers
        import desklib.receivers