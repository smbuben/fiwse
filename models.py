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

from google.appengine.ext import ndb
from google.appengine.api import users
import re


class CountryData:
    """
    Container for the base information about participating nations.
    """

    def __init__(self):
        rawdata = [
            ('South Korea',     72.82,   62),
            ('Austria',         52.92,  123),
            ('Netherlands',     52.22,   51),
            ('Norway',          49.45,  125),
            ('Germany',         44.03,  157),
            ('United States',   38.80,  260),
            ('Russia',          36.91,  209),
            ('Canada',          35.05,  224),
            ('Sweden',          26.36,  112),
            ('China',           23.45,   60),
            ('Switzerland',     21.96,  167),
            ('Croatia',         21.05,   11),
            ('France',          19.82,  107),
            ('Estonia',         18.04,   24),
            ('Australia',       14.64,   58),
            ('Poland',          13.46,   55),
            ('Finland',         12.54,  110),
            ('Italy',           11.16,  110),
            ('Czech Republic',  10.76,   84),
            ('Japan',            7.81,  115),
            ('Belarus',          6.87,   25),
            ('Slovenia',         5.42,   78),
            ('Slovakia',         5.31,   63),
            ('Great Britain',    5.06,   64),
            ('Latvia',           3.50,   56),
            ('Bulgaria',         1.98,   16),
            ('Kazakhstan',       1.33,   45),
            ('Albania',          1.00,    1),
            ('Algeria',          1.00,    1),
            ('Andorra',          1.00,    6),
            ('Argentina',        1.00,    9),
            ('Armenia',          1.00,    4),
            ('Azerbaijan',       1.00,    3),
            ('Belgium',          1.00,   16),
            ('Bosnia and Herzegovina', 1.00, 5),
            ('Brazil',           1.00,   10),
            ('British Virgin Islands', 1.00, 1),
            ('Cayman Islands',   1.00,    1),
            ('Chile',            1.00,    6),
            ('Cyprus',           1.00,    1),
            ('Denmark',          1.00,   15),
            ('Georgia',          1.00,    4),
            ('Greece',           1.00,    5),
            ('Hong Kong',        1.00,    1),
            ('Hungary',          1.00,   16),
            ('Iceland',          1.00,    5),
            ('India',            1.00,    3),
            ('Iran',             1.00,    5),
            ('Ireland',          1.00,    4),
            ('Israel',           1.00,    5),
            ('Jamaica',          1.00,    2),
            ('Kyrgyzstan',       1.00,    1),
            ('Lebanon',          1.00,    2),
            ('Liechtenstein',    1.00,    8),
            ('Lithuania',        1.00,    9),
            ('Luxembourg',       1.00,    2),
            ('Macedonia',        1.00,    3),
            ('Malta',            1.00,    1),
            ('Mexico',           1.00,    1),
            ('Moldova',          1.00,    5),
            ('Monaco',           1.00,    5),
            ('Mongolia',         1.00,    2),
            ('Montenegro',       1.00,    1),
            ('Morocco',          1.00,    2),
            ('Nepal',            1.00,    1),
            ('New Zealand',      1.00,   22),
            ('Pakistan',         1.00,    1),
            ('Paraguay',         1.00,    1),
            ('Peru',             1.00,    1),
            ('Philippines',      1.00,    1),
            ('Portugal',         1.00,    1),
            ('Puerto Rico',      1.00,    1),
            ('Romania',          1.00,   17),
            ('San Marino',       1.00,    1),
            ('Serbia',           1.00,    9),
            ('Spain',            1.00,   18),
            ('Chinese Taipei',   1.00,    2),
            ('Tajikistan',       1.00,    1),
            ('Thailand',         1.00,    1),
            ('Togo',             1.00,    1),
            ('Tonga',            1.00,    1),
            ('Timor-Leste',      1.00,    1),
            ('Turkey',           1.00,    6),
            ('Ukraine',          1.00,   42),
            ('Uzbekistan',       1.00,    3),
            ('Virgin Islands',   1.00,    1),
            ('Zimbabwe',         1.00,    1)
        ]
        self.mapping = dict()
        for idx, data in enumerate(rawdata):
            name, cost, athletes = data
            self.mapping[idx] = dict(name=name, cost=cost, athletes=athletes)
        self.inv_mapping = {v['name']: k for k, v in self.mapping.iteritems()}

    def get_mapping(self):
        return self.mapping

    def get_name_by_idx(self, idx):
        return self.mapping[idx]['name']

    def get_cost_by_idx(self, idx):
        return self.mapping[idx]['cost']

    def get_athletes_by_idx(self, idx):
        return self.mapping[idx]['athletes']

    def get_athletes_by_name(self, name):
        return self.get_athletes_by_idx(self.inv_mapping[name])

    def calculate_points_by_idx(self, idx, results):
        gold, silver, bronze = results
        return float(300*gold + 200*silver + 100*bronze) / self.mapping[idx]['athletes']

    def calculate_points_by_name(self, name, results):
        return self.calculate_points_by_idx(self.inv_mapping[name], results)

Countries = CountryData()


class League(ndb.Model):
    """
    Ancestor for all teams to ensure consistency.
    """
    pass


def validate_not_empty_string(prop, value):
    value = re.sub(r'[^-a-zA-Z0-9 _.,!?]', '', value)
    value = value[:40]
    if value == '':
        raise Exception
    return value

def validate_countries(prop, value):
    if not type(value) is list or len(value) != 5:
        raise Exception
    value = [int(x) for x in value]
    total = 0.0
    for idx in value:
        # This will raise an exception if idx is invalid.
        total += Countries.get_cost_by_idx(idx)
    if total > 100.00:
        raise Exception
    return value


class Team(ndb.Model):
    """
    Participating team.
    """
    owner = ndb.UserProperty(
        required=True,
        indexed=True)
    manager = ndb.StringProperty(
        validator=validate_not_empty_string,
        required=True,
        indexed=False)
    # Not using repeated integers to streamline validation.
    countries = ndb.PickleProperty(
        validator=validate_countries,
        required=True,
        indexed=False)

    @classmethod
    def get(cls):
        """
        Get a user's team.
        """
        user = users.get_current_user()
        key = ndb.Key(League, 'default', Team, user.user_id())
        return key.get()

    @classmethod
    def update(cls, manager, countries):
        """
        Update (create if neccessary) a user's team.
        """
        user = users.get_current_user()
        key = ndb.Key(League, 'default', Team, user.user_id())
        team = key.get()
        if not team:
            team = cls(
                key=key,
                owner=user,
                manager=manager,
                countries=countries)
        else:
            team.populate(
                manager=manager,
                countries=countries)
        team.put()

    @classmethod
    def update_manager_only(cls, manager):
        """
        Update the manager name of an already created user's team.
        """
        user = users.get_current_user()
        key = ndb.Key(League, 'default', Team, user.user_id())
        team = key.get()
        team.populate(manager=manager)
        team.put()

    @classmethod
    def delete(cls):
        """
        Delete a user's team.
        """
        team = cls.get()
        team.key.delete()

    @classmethod
    def getall(cls):
        """
        Get all teams. All of them.
        """
        root = ndb.Key(League, 'default')
        return cls.query(ancestor=root).fetch()


class Results(ndb.Model):
    """
    Current scores for the countries.
    """
    medals = ndb.PickleProperty(
        required=True,
        indexed=False)
    timestamp = ndb.DateTimeProperty(
        required=True,
        indexed=False,
        auto_now=True)

    @classmethod
    def get(cls):
        """
        Retrieve the stored results.
        """
        key = ndb.Key(Results, 'default')
        return key.get()

    @classmethod
    def update(cls, medals):
        """
        Update (create if necessary) the stored results.
        """
        key = ndb.Key(Results, 'default')
        results = key.get()
        if not results:
            results = cls(
                key=key,
                medals=medals)
        else:
            results.populate(medals=medals)
        results.put()


