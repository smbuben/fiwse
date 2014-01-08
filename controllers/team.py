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
