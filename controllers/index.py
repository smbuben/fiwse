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

