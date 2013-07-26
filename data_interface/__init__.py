import os
import pickle
import httplib2
import re
import urllib2

from apiclient.http import MediaFileUpload
from apiclient.discovery import build

from apiclient import errors

import ghost_db
import thedriver

db_connector = ghost_db.GhostDBConnector();

class UserSession:
        name = None
        service = None

        def __init__(self, user_name):
                pass

def list_ghost_docs( user_id ):
        pass

def list_google_docs( user_id, if_hide_ghost_doc=True ):
        # look up user's google id from d/b.
        # look up user's auth.
        # list docs.
        pass

def list_recent_docs( user_id ):
        pass

def add_user( user_name, google_account, oauth_code):
        user = ghost_db.User(name=user_name,
                        google_account=google_account,
                        oauth_code=oauth_code)
        db_connector.session.add(user)

