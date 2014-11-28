# import requests
import urllib
import json


class APIClient(object):
    """Creates an API client object

    :param userid: the API userid found in the control panel
    :param api_key: the API key found in the control panel Settings > API

    """
    def __init__(self, userid=None, api_key=None, base_url=None):
        # userid and api key sent with every request
        self.userid = userid
        self.key = api_key

        # the base production api url
        self.base_url = base_url

        # the error description if it occured
        self.error = None

    def request(self, method='GET', path=None, params=None):
        """
        Makes a request to the API with the given parameters

        :param method: the HTTP method to use
        :param path: the api path to request
        :param params: the parameters to be sent
        """
        # the api request result
        result = None

        args = urllib.urlencode(params)
        completeURL = self.base_url + path + '.json?' + args
        print "Invoking >" + completeURL + "<..."

        try:
            data = urllib.urlopen(completeURL)
            # send a request to the api server
            """
            r = requests.request(
                    method = method,
                    url = completeURL,
                    params = params,
                    headers = { 'User-Agent': 'Python API Client' }
                )

            # raise an exception if status code is not 200
            if r.status_code is not 200:
                raise Exception
            else:
                result = r.json()
            """
            result = json.loads(data.read())
        except Exception:
            self.error = 'An unexpected error occurred.'

        return result
