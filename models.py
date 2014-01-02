from google.appengine.ext import ndb
from google.appengine.api import users
import re


class CountryData:
    """
    Container for the base information about participating nations.
    """

    def __init__(self):
        rawdata = [
            ('South Korea',     69.80,   62),
            ('Austria',         51.60,  123),
            ('Netherlands',     50.65,   51),
            ('Norway',          48.29,  125),
            ('Germany',         44.06,  157),
            ('United States',   38.68,  260),
            ('Russia',          36.95,  209),
            ('Canada',          35.01,  224),
            ('Sweden',          26.36,  112),
            ('China',           24.03,   60),
            ('Croatia',         23.39,   11),
            ('Switzerland',     22.04,  167),
            ('France',          19.83,  107),
            ('Estonia',         18.00,   24),
            ('Australia',       15.03,   58),
            ('Poland',          13.50,   55),
            ('Finland',         12.58,  110),
            ('Italy',           11.10,  110),
            ('Czech Republic',  10.74,   84),
            ('Japan',            7.86,  115),
            ('Belarus',          6.80,   25),
            ('Slovenia',         5.70,   78),
            ('Slovakia',         5.28,   63),
            ('Great Britain',    5.24,   64),
            ('Latvia',           3.48,   56),
            ('Bulgaria',         1.91,   16),
            ('Kazakhstan',       1.32,   45),
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
            ('India',            1.00,    2),
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


