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
        if not self.season_active:
            try:
                models.Team.update(
                    self.request.get('manager'),
                    self.request.get_all('countries'))
            except:
                self.flash(
                    'Team not updated. Manager must not be blank and 5 '
                    'countries whose total cost is less than $100.00 must '
                    'be chosen.')
            else:
                self.flash('Team updated successfully!', self.flash_success)
        else:
            try:
                models.Team.update_manager_only(
                    self.request.get('manager'))
            except:
                self.flash('Team not updated. Manager must not be blank.')
            else:
                self.flash('Team updated successfully!', self.flash_success)
        self.go('/team')
