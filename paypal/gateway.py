import requests
import time
import urllib
import urlparse


def post(url, params):
    """
    Make a POST request to the URL using the key-value pairs.  Return
    a set of key-value pairs.
    """
    for k in params.keys():
        if type(params[k]) == unicode:
            params[k] = params[k].encode('utf-8')
    payload = urllib.urlencode(params.items())

    # Make request
    start_time = time.time()
    response = requests.post(url, payload)
    if response.status_code != requests.codes.ok:
        raise RuntimeError("Unable to communicate with PayPal")

    # Convert response into a simple key-value format
    pairs = {}
    for key, values in urlparse.parse_qs(response.content).items():
        pairs[key] = values[0]

    # Add audit information
    pairs['_raw_request'] = payload
    pairs['_raw_response'] = response.content
    pairs['_response_time'] = (time.time() - start_time) * 1000.0

    return pairs
