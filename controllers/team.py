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
        try:
            models.Team.update(
                self.request.get('manager'),
                self.request.get_all('countries'))
        except:
            self.flash(
                'Your team was not updated. The manager field must not be '
                'empty, and you must choose 5 countries whose total cost is '
                'less than $100.00.')
        else:
            self.flash('Your team was updated successfully!', self.flash_success)
        self.go('/team')
