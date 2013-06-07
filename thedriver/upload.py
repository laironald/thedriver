# this file contains functions for uploading files to google drive

import os
import pickle
import httplib2
import re
import urllib2
from apiclient.discovery import build

class uploader():
    driver = None
    folderLink = None

    def find_public_folder(self, folder_name):
        files = self.driver.files(title=folder_name)
        files = filter(
          lambda x: x['mimeType'] == 'application/vnd.google-apps.folder'
            and (not 'explicitlyTrashed' in x or not x['explicitlyTrashed']) 
	    and 'webViewLink' in x,
          files)
        return files

    def create_public_folder(self, folder_name="publish_folder"):
        import thedriver
        if self.driver.service==None:
            self.driver.build()
        body = { 
		'title': folder_name, 
		'mimeType': 'application/vnd.google-apps.folder'
	       }
        file = service.files().insert(body=body).execute()
        permission = {
                      'value': '',
                      'type': 'anyone',
                      'role': 'reader'
                     }
        
        service.permissions().insert(
        fileId=file['id'], body=permission).execute()
        return file
        
    def __init__(self, driver=None, folder_name="publish_folder"):
        import thedriver
        if driver == None:
            self.driver = thedriver.go()
	    self.driver.build()
        folders = self.find_public_folder(folder_name)
	if len(folders) == 0:
		create_public_folder(folder_name)
		folders = self.find_public_folder(folder_name)
        self.folderLink = folders[0]['webViewLink']

