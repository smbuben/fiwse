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

    def __init__(self, name, results):
        self.name = name
        self.gold, self.silver, self.bronze = results
        if name == 'not available':
            self.athletes = 0
            self.points = 0.0
        else:
            self.athletes = \
                models.Countries.get_actual_athletes_by_name(name)
            self.points = \
                models.Countries.calculate_points_by_name(name, results)


class Handler(base.RequestHandler):

    def get(self):
        cache_val = memcache.get('all_country_scores')
        if not cache_val:
            results = models.Results.get()
            if not results:
                country_scores = [Score('not available', (0, 0, 0))]
                timestamp = datetime.datetime.utcnow()
            else:
                country_scores = list()
                for country in results.medals.keys():
                    country_scores.append(
                        Score(
                            country,
                            results.medals[country]))
                timestamp = results.timestamp
            country_scores.sort(key=lambda x: x.points, reverse=True)
            memcache.add('all_country_scores', (country_scores, timestamp), 900)
        else:
            country_scores, timestamp = cache_val
        template_vals = {
            'countries' : country_scores,
            'timestamp' : timestamp,
        }
        self.render('medals.html', **template_vals)

