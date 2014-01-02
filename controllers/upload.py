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
