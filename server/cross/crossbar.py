from twisted.internet.defer import inlineCallbacks

from autobahn.twisted.wamp import ApplicationSession
from autobahn.wamp.exception import ApplicationError

from importlib import import_module

import django
django.setup()


def django_session(cookie_string):
    from django.http import parse_cookie
    from django.conf import settings
    cookie = parse_cookie(cookie_string)
    session_key = cookie[settings.SESSION_COOKIE_NAME]
    engine = import_module(settings.SESSION_ENGINE)
    return engine.SessionStore(session_key)


def django_user(cookie_string):
    from django.conf import settings
    from django.contrib import auth

    session = django_session(cookie_string)
    user_id = auth.get_user_model()._meta.pk.to_python(
        session[auth.SESSION_KEY])
    backend_path = session[auth.BACKEND_SESSION_KEY]
    if backend_path in settings.AUTHENTICATION_BACKENDS:
        return auth.load_backend(backend_path).get_user(user_id)


def user_from_details(realm, authid, details):
    # TODO : realm check, username == authid check
    cookie_string = details.get('transport', {}).get(
        'http_headers_received', {}).get('cookie', None)
    if cookie_string:
        try:
            user = django_user(cookie_string)
            if user:
                return {
                    'username': user.username, 'role': 'frontend',
                    'secret': user.socketuser.key}
        except:
            import traceback
            print(traceback.format_exc())


# http://crossbar.io/docs/WAMP-CRA-Authentication/#dynamic-credentials

class AppAuthn(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):

        def authenticate(realm, authid, details):
            user = user_from_details(realm, authid, details)
            if user:
                return user

            raise ApplicationError(
                "jp.lafoglia.no_such_user",
                "could not authenticate session "
                "- no such user {}".format(authid))

        try:
            yield self.register(authenticate, 'jp.lafoglia.authn')
        except Exception as e:
            print("could not register "
                  "custom WAMP-CRA authenticator: {0}".format(e))


# http://crossbar.io/docs/Authorization/
class AppAuthz(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):
        try:
            yield self.register(self.authorize, 'jp.lafoglia.authz')
        except Exception as e:
            print("MyAuthorizer: "
                  "failed to register authorizer procedure ({})".format(e))

    def authorize(self, session, uri, action):
        from cross.models import Topic
        username = session.get('authid', '')
        topic = Topic.objects.filter(uri=uri).first()
        return topic and topic.is_authorized(username, action) or False
