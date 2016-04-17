import os
import json
import requests
import random
import hmac
import hashlib
import base64
from six.moves.urllib import parse
from datetime import datetime


class BaseMessage(object):

    def __init__(self, data):
        if isinstance(data, basestring):
            self.data = json.loads(data)
        elif isinstance(data, dict):
            self.data = data
        else:
            self.data = {}

    def __getattr__(self, name):
        return self.data.get(name, None)


class Config(BaseMessage):

    @property
    def workers(self):
        return [Worker(i) for i in(self.data['workers'])]

    @property
    def default_transport(self):
        return self.workers[0].transports[0]


class Worker(BaseMessage):

    @property
    def transports(self):
        return [Transport(i) for i in(self.data['transports'])]


class Transport(BaseMessage):
    pass

    @property
    def publishers(self):
        return [
            Path(self, p, k) for p, k in self.data['paths'].items()
            if k['type'] == 'publisher']

    @property
    def endpoint(self):
        return BaseMessage(self.data['endpoint'])


class Path(BaseMessage):
    def __init__(self, transport, path, data):
        super(Path, self).__init__(data)
        self.path = path
        self.transport = transport

    @property
    def options(self):
        def _cache():
            self._options = BaseMessage(self.data['options'])
            return self._options
        return getattr(self, '_options', _cache())

    def publish(self, topic, *args, **kwargs):
        endpoint = "http://localhost:{0}/{1}".format(
            self.transport.endpoint.port,
            self.path,
        )

        data = {"topic": topic}
        if args:
            data['args'] = list(args)
        if kwargs:
            data['kwargs'] = kwargs

        if self.options.key and self.options.secret:
            queries = signature_parameters(
                self.options.key, self.options.secret, data)
            endpoint = "{0}?{1}".format(endpoint, queries)

        requests.post(endpoint, json=data)


def load():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    CONF_FILE = os.path.join(BASE_DIR, ".crossbar/config.json")

    return Config(json.load(open(CONF_FILE)))


def _utcnow():
    now = datetime.utcnow()
    return now.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


def signature_parameters(key, secret, body, seq=1):
    params = {
        'key': key,
        'timestamp': _utcnow(),
        'seq': seq,
        'nonce': random.randint(0, 9007199254740992),

    }
    # HMAC[SHA256]_{secret} (key | timestamp | seq | nonce | body) => signature
    hm = hmac.new(secret.encode('utf8'), None, hashlib.sha256)
    hm.update(params['key'].encode('utf8'))
    hm.update(params['timestamp'].encode('utf8'))
    hm.update(u"{0}".format(params['seq']).encode('utf8'))
    hm.update(u"{0}".format(params['nonce']).encode('utf8'))
    # hm.update(json.dumps(body, separators = (',', ':')))
    hm.update(json.dumps(body))
    params['signature'] = base64.urlsafe_b64encode(hm.digest())

    return parse.urlencode(params)
