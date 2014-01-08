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

from google.appengine.api import memcache
import base
import models
import datetime


class Score:

    def __init__(self, owner, manager, countries, results):
        self.owner = owner
        self.manager = manager
        self.details = ', '.join(
            [models.Countries.get_name_by_idx(x) for x in countries])
        points = 0.0
        for idx in countries:
            name = models.Countries.get_name_by_idx(idx)
            if results and results.medals.has_key(name):
                points += models.Countries.calculate_points_by_idx(
                    idx,
                    results.medals[name])
        self.points = points


class Handler(base.RequestHandler):

    def get(self):
        cache_val = memcache.get('all_teams_scores')
        if cache_val is None:
            team_scores = list()
            teams = models.Team.getall()
            results = models.Results.get()
            for team in teams:
                team_scores.append(
                    Score(
                        team.owner,
                        team.manager,
                        team.countries,
                        results))
            team_scores.sort(key=lambda x: x.points, reverse=True)
            timestamp = datetime.datetime.utcnow()
            memcache.add('all_teams_scores', (team_scores, timestamp), 900)
        else:
            team_scores, timestamp = cache_val
        template_vals = {
            'teams' : team_scores,
            'timestamp' : timestamp,
        }
        self.render('scores.html', **template_vals)

