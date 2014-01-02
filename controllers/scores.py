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
            memcache.add('all_teams_scores', (team_scores, timestamp), 3600)
        else:
            team_scores, timestamp = cache_val
        template_vals = {
            'teams' : team_scores,
            'timestamp' : timestamp,
        }
        self.render('scores.html', **template_vals)

