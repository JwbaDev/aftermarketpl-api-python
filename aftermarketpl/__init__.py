from threading import Thread
import requests
from requests.auth import HTTPBasicAuth
import logging
import contextlib

try:
  from http.client import HTTPConnection # py3
except ImportError:
  from httplib import HTTPConnection # py2

class APIException(Exception):
  def __init__(self, status, message='Unknown HTTP Error'):
    self.status = status
    self.message = message

  def __str__(self):
    return str(self.status) + ": " + self.message

def throw(e): raise e

class Client(object):

  def __init__(self, key, secret, debug=False, url='https://json.aftermarket.pl'):
    self.url = url
    self.key = key
    self.secret = secret
    self.debug = debug

  @property
  def debug(self):
    return self._debug

  @debug.setter
  def debug(self, enabled):
    logging.basicConfig() # you need to initialize logging, otherwise you will not see anything from requests
    requests_log = logging.getLogger("urllib3")
    #logging.getLogger().setLevel(logging.DEBUG)
    if enabled:
      requests_log.setLevel(logging.DEBUG)
      requests_log.propagate = True
    else:
      requests_log.setLevel(logging.WARNING)
      requests_log.propagate = False

  def send_async(self, path, params = {}, callback = lambda x: None, reject = throw):
    p = Thread(target=self.send, args = (path, params, callback, reject))
    p.start()

  def send(self, path, params = {}, callback = lambda x: None, reject = throw):
    try:
      resp = requests.post(self.url + path, auth=HTTPBasicAuth(self.key, self.secret), data=params)
      resp.raise_for_status()
      json = resp.json()
      if json['status'] >= 400: raise APIException(json['status'], json.get('error'))
      callback(json['data'])
    except Exception as e:
      reject(e)
    return json['data']
