import requests
import hashlib
import hmac
import time
import os
from operator import itemgetter

SECRETKEY = os.environ["SECRETKEY"]
URL =  os.environ["API_URL"]
APIKEY = os.environ["APIKEY"]
HEADERS = {'X-MBX-APIKEY': APIKEY}

def _order_params(data):
    """Convert params to list with signature as last element
    :param data:
    :return:
    """
    data = dict(filter(lambda el: el[1] is not None, data.items()))
    has_signature = False
    params = []
    for key, value in data.items():
        if key == 'signature':
            has_signature = True
        else:
            params.append((key, str(value)))
    # sort parameters by key
    params.sort(key=itemgetter(0))
    if has_signature:
        params.append(('signature', data['signature']))
    return params

def generate_query_string(params):
    query_string = '&'.join([f"{d[0]}={d[1]}" for d in params])
    return query_string

def _generate_signature(data) -> str:
    params = _order_params(data) 
    query_string = generate_query_string(params)
    print(params, query_string, 'string')
    m = hmac.new(SECRETKEY.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256)
    return m.hexdigest()


kwargs = {'timestamp': int(time.time() * 1000)}
kwargs['signature'] = _generate_signature(kwargs)

session = requests.session()
session.headers.update(HEADERS)

params = _order_params(kwargs) 
args = {'params': generate_query_string(params)}
response = getattr(session, 'get')(URL, **args)

print(response)
print(response.json())