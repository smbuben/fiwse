from google.appengine.api import memcache
import base
import models


class Score:

    def __init__(self, name, results):
        self.name = name
        self.gold, self.silver, self.bronze = results
        if name == 'not available':
            self.points = 0.0
        else:
            self.points = \
                models.Countries.calculate_points_by_name(name, results)


class Handler(base.RequestHandler):

    def get(self):
        country_scores = memcache.get('all_country_scores')
        if not country_scores:
            results = models.Results.get()
            if not results:
                country_scores = [Score('not available', (0, 0, 0))]
            else:
                country_scores = list()
                for country in results.medals.keys():
                    country_scores.append(
                        Score(
                            country,
                            results.medals[country]))
            country_scores.sort(key=lambda x: x.points, reverse=True)
            memcache.add('all_country_scores', country_scores, 10)
        template_vals = {
            'countries' : country_scores,
        }
        self.render('medals.html', **template_vals)

