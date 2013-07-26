import inspect
import os
import pickle
import httplib2
from apiclient.discovery import build

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
pickle_file = "{}/{}".format(current_dir, "../pickle/oauth_code.pick")
#TODO: add some sense of relativity here


class go():
    http = None
    service = None

    def __init__(self, product="drive", version="v2"):
        self.product = product
        self.version = version
        pass

    def build(self, **kwargs):
        """
        Very basic way to check if an authentication exists. We are pickling
        items and their objects. Likely to change this way of authentication

        Tested? No
        """
        if os.path.exists(pickle_file):
            credentials = pickle.load(open(pickle_file, "rb"))
            http = httplib2.Http()
            http = credentials.authorize(http)
        else:
            http = None
        self.http = http

        if not self.http:
            self.auth_http()
        kwargs["http"] = self.http
        self.service = build(self.product, self.version, **kwargs)
        return self.service

    def files(self, **kwargs):
        """
        maxResults	integer
          Maximum number of files to return.
          Acceptable values are 0 to 1000, inclusive. (Default: 100)
        pageToken	string
          Page token for files.
        q	string
          Query string for searching files.
          See Searching for files for more information about supported fields and operations.
          See: https://developers.google.com/drive/search-parameters
        """
        if not self.service:
            self.build()
        #i suspect we may search for title quite a bit
        if "title" in kwargs:
            kwargs["q"] = "title contains '" + kwargs.pop("title") + "'"

        result = []
        while True:
            try:
                files = self.service.files().list(**kwargs).execute()
                result.extend(files['items'])
                page_token = files.get('nextPageToken')
                if not page_token:
                    break
                kwargs['pageToken'] = page_token
            except:
                break
        return result
