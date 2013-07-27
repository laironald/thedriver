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

db_connector = ghost_db.GhostDBConnector()
gdoc_mimeType = 'application/vnd.google-apps.document' 

class UserSession:
        drive = None
        name = None

        def __init__(self, user_name=None):
                self.name = user_name
                self.drive = thedriver.go()
                self.drive.build()

def list_ghost_docs( user_id ):
        pass

def list_google_docs( user_id=None, if_hide_ghost_doc=True ):
        """list a user's all editable google docs
        
        Args:
            user_id: user's GhostDocs id
            if_hide_ghost_doc: if remove docs already exist in ghost docs from the list

        Returns:
            A list of metadata of editable google docs.

            examples:
            [ {u'mimeType':u'application/vnd.google-apps.document',
              u'title':u'Test' ... },
              {...}
            ]

        """
        files = session.drive.files();
        google_docs = filter( lambda f: f['mimeType'] == gdoc_mimeType
                        and (not 'explicitlyTrashed' in f
                                or not f['explicitlyTrashed'])
                        and f['editable'],
                        files)
        return google_docs

def list_recent_docs( user_id ):
        pass

def load_doc( user_id, google_doc_id ):
        file = session.drive.service.files().get(fileId=google_doc_id).execute()
        return file
        
def add_user( user_name, google_account, oauth_code):
        user = ghost_db.User(name=user_name,
                        google_account=google_account,
                        oauth_code=oauth_code)
        db_connector.session.add(user)

session = UserSession();
