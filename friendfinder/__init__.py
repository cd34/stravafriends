from pyramid.config import Configurator
from pyramid.interfaces import ISessionFactory
from pyramid.session import UnencryptedCookieSessionFactoryConfig

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.set_session_factory( \
           UnencryptedCookieSessionFactoryConfig( \
           settings.get('session_secret')))
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('friends', '/friends/:id')
    config.add_route('strava_id', '/strava_id/:id')
    config.scan()
    return config.make_wsgi_app()
