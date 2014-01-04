import webapp2
import webapp2_extras.jinja2
import os
import logging


class Defaults:
    """
    Default configuration values to use in the event that the private
    configuration module is not available.
    """

    # Default session cookie key.
    session_cookie_key = ''

    # Default salt value.
    salt = ''

    def __init__(self):
        logging.warn('Using built-in default configuration.')
        logging.warn('Create a custom private configuration to fix.')


# Try to load the private configuration module.
# Fallback to defaults if unavailable.
try:
    import private
except:
    private = Defaults()


wsgi_config = {
    'webapp2_extras.sessions':
        {
            'secret_key' : private.session_cookie_key,
            'cookie_args' :
                {
                    'httponly' : True,
                },
        },
    'webapp2_extras.jinja2' :
        {
            'template_path' : 'views',
        },
    'private_salt' : private.salt,
    }

wsgi_debug = os.environ.get('SERVER_SOFTWARE', '').startswith('Dev')


default_app = webapp2.WSGIApplication(
    [
        webapp2.Route(
            r'/upload',
            'controllers.upload.Handler'),
        webapp2.Route(
            r'/',
            'controllers.index.Handler'),
    ],
    config=wsgi_config,
    debug=wsgi_debug)


iface_app = webapp2.WSGIApplication(
    [
        webapp2.Route(
            r'/ui/logout',
            'controllers.logout.Handler'),
        webapp2.Route(
            r'/ui/about',
            'controllers.about.Handler'),
        webapp2.Route(
            r'/ui/team',
            'controllers.team.Handler'),
        webapp2.Route(
            r'/ui/scores',
            'controllers.scores.Handler'),
        webapp2.Route(
            r'/ui/medals',
            'controllers.medals.Handler'),
    ],
    config=wsgi_config,
    debug=wsgi_debug)

