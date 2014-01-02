import base

class Handler(base.RequestHandler):

    def get(self):
        template_vals = {}
        self.render('about.html', **template_vals)

