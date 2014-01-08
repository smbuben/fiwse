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


PUBLIC_KEY="""-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA0AQHT3+/jcQGX0pH/bVj
32ACg/5yN9e2S4TaQGyjsJts8feqN2FOPHQV9lLm91jN7dh0z8ggt6f1oMuTfMgX
estpeNZbc1WBhT7fCqtdsTk+PqJ3YesNorUGkW+4rpEREuipIJbzYorfNhwSI4rI
Pr73YNdKiVHQPnLB4d5jRhk09RxQAWz9VPxbXMsRC8MvH1JEQ/Fq7FvAxBQEWhzL
DEkHAWatHZKReXiYlbktkjsIJhjd65fHSfNqMpVrUeLo+JJLYnYCMHNM77e0l8wp
Vuq8dtyAFVmF46PNjZqClrihXYFHWMZw5QDsWh5dG45NqVms3kF+ScCDhD6tpvqa
LQIDAQAB
-----END PUBLIC KEY-----"""

class Handler(webapp2.RequestHandler):

    def post(self):
        message = base64.b64decode(self.request.get('message'))
        signature = base64.b64decode(self.request.get('signature'))
        key = RSA.importKey(PUBLIC_KEY)
        sha = SHA.new(message)
        verifier = PKCS1_v1_5.new(key)
        if not verifier.verify(sha, signature):
            raise Exception

        medals = pickle.loads(message)
        models.Results.update(medals=medals)
