import base
import google.appengine.api.users


class Handler(base.RequestHandler):

    def get(self):
        self.session.clear()
        self.redirect(google.appengine.api.users.create_logout_url('/'))

