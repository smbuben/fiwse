#
# This file is part of the fiwse project.
#
# Copyright (C) 2014 Stephen M Buben <smbuben@gmail.com>
#
# fiwse is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# fiwse is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with fiwse.  If not, see <http://www.gnu.org/licenses/>.
#

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

    # Default public key (cannot upload data without this).
    public_key = ''

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
    'public_key' : private.public_key,
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

