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

from google.appengine.api import users
import webapp2
import webapp2_extras.jinja2


class Handler(webapp2.RequestHandler):

    @webapp2.cached_property
    def jinja2(self):
        # Return a Jinja2 render cached in the app registry.
        return webapp2_extras.jinja2.get_jinja2(app=self.app)

    def get(self):
        if users.get_current_user():
            return self.redirect('/ui/about')
        template_vals = {
            'login_url' : users.create_login_url('/ui/about')
        }
        view = self.jinja2.render_template('index.html', **template_vals)
        self.response.write(view)

