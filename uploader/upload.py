#!/usr/bin/env python
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

import argparse
import base64
import pickle
import urllib
from bs4 import BeautifulSoup
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Upload data to a fiwse instance.')
    parser.add_argument(
        '-s', '--src',
        action='store', dest='src', type=str,
        default='https://en.wikipedia.org/wiki/2014_Winter_Olympics_medal_table',
        help='Read Wikipedia score data from URL. Default: https://en.wikipedia.org/wiki/2014_Winter_Olympics_medal_table')
    parser.add_argument(
        '-d', '--dst',
        action='store', dest='dst', type=str,
        default='http://localhost:8080/upload',
        help='Upload score data to URL. Default: http://localhost:8080/upload')
    parser.add_argument(
        '-k', '--keyfile',
        action='store', dest='keyfile', type=str,
        default='private.pem',
        help='Sign upload with PEM format private key. Default: private.pem')
    parser.add_argument(
        '-f', '--scorefile',
        action='store', dest='scorefile', type=str,
        default=None,
        help='Read Wikipedia score data from file instead of the network.')
    parser.add_argument(
        '-p', '--pretend',
        action='store_true', dest='pretend',
        help='Do not actually upload score data.')
    args = parser.parse_args()

    #
    # Get the raw HTML.
    #

    if not args.scorefile:
        print 'Retrieving scores from %s' % (args.src)
        inf = urllib.urlopen(args.src)
        if 200 != inf.getcode():
            raise Exception('Score data request received error status.')
        html = inf.read()
        inf.close()
    else:
        print 'Retrieving scores from %s' % (args.scorefile)
        with open(args.scorefile) as inf:
            html = inf.read()

    #
    # Get the results.
    #

    soup = BeautifulSoup(html)
    # The medal table should be the second table on this page.
    # TODO: This lazy strategy may need to be revisited.
    table = soup.find_all('table')[1]
    results = dict()
    # The first and last rows are the header and the totals.
    # The last four columns contain the contry name (as a link) and the
    # gold, silver, and bronze totals.
    for row in table.find_all('tr')[1:-1]:
        nation, gold, silver, bronze = row.find_all('td')[-5:-1]
        results[nation.a.string.encode('ascii')] = \
            (int(gold.string), int(silver.string), int(bronze.string))
    print 'Scores:'
    for k, v in results.iteritems():
        print k, v

    #
    # Create a signed message.
    #

    message = pickle.dumps(results)
    with open(args.keyfile) as inf:
        key = RSA.importKey(inf)
    sha = SHA.new(message)
    signer = PKCS1_v1_5.new(key)
    signature = signer.sign(sha)

    #
    # Upload to fiwse instance.
    #

    if not args.pretend:
        print 'Uploading scores to %s' % (args.dst)
        params = urllib.urlencode({
            'message' : base64.b64encode(message),
            'signature' : base64.b64encode(signature),
        })
        inf = urllib.urlopen(args.dst, params)
        print 'Response: %d' % (inf.getcode())
    else:
        print 'Pretend mode enabled. Not uploading to %s' % (args.dst)

