import os


def webapp_add_wsgi_middleware(app):
    # Enable appstats on the development server but not in production.
    if os.environ.get('SERVER_SOFTWARE', '').startswith('Dev'):
        from google.appengine.ext.appstats import recording
        app = recording.appstats_wsgi_middleware(app)
    return app

