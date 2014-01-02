import base
import models


class Handler(base.RequestHandler):

    def get(self):
        template_vals = {
            'team' : models.Team.get(),
            'countries' : models.Countries.get_mapping(),
        }
        self.render('team.html', **template_vals)

    def post(self):
        models.Team.update(
            self.request.get('manager'),
            self.request.get_all('countries'))
        self.go('/team')
