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

import webapp2
import models
import base64
import pickle
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA


class Handler(webapp2.RequestHandler):

    def post(self):
        message = base64.b64decode(self.request.get('message'))
        signature = base64.b64decode(self.request.get('signature'))
        key = RSA.importKey(self.app.config.get('public_key'))
        sha = SHA.new(message)
        verifier = PKCS1_v1_5.new(key)
        if not verifier.verify(sha, signature):
            raise Exception('Uploaded data signature verification failed.')

        medals = pickle.loads(message)
        models.Results.update(medals=medals)
