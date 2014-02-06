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


class ActiveCountry:

    def __init__(self, idx, results):
        self.name = models.Countries.get_name_by_idx(idx)
        self.cost = models.Countries.get_cost_by_idx(idx)
        self.actual_athletes = \
            models.Countries.get_actual_athletes_by_idx(idx)
        self.projected_athletes = \
            models.Countries.get_projected_athletes_by_idx(idx)
        if results and results.medals.has_key(self.name):
            medals = results.medals[self.name]
            self.gold, self.silver, self.bronze = medals
            self.points = models.Countries.calculate_points_by_idx(idx, medals)
        else:
            self.gold = self.silver = self.bronze = 0
            self.points = 0.0


class Handler(base.RequestHandler):

    def get(self):
        if not self.season_active:
            template_vals = {
                'team' : models.Team.get(),
                'countries' : models.Countries.get_mapping(),
            }
            self.render('team.html', **template_vals)
        else:
            team = models.Team.get()
            if team:
                results = models.Results.get()
                selections = list()
                for idx in models.Team.get().countries:
                    selections.append(ActiveCountry(idx, results))
                total_points = 0.0
                for country in selections:
                    total_points += country.points
            else:
                selections = None
                total_points = 0.0
            template_vals = {
                'team' : team,
                'selections' : selections,
                'total_points' : total_points,
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
