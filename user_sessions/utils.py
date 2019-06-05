from user_sessions.models import UserSession


def delete_user_sessions(user):
    user_sessions = UserSession.objects.filter(user = user)
    for user_session in user_sessions:
        user_session.session.delete()