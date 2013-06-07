# this file contains functions for uploading files to google drive

import os
import pickle
import httplib2
import re
import urllib2

from apiclient.http import MediaFileUpload
from apiclient.discovery import build

class uploader():
    driver = None
    uploadFolder = None

    def find_publish_folder(self, folder_name):
        '''Check if there exists any public folder whose name contains folder_name.
	Args:
	folder_name: keywords of public folder's name.

	Returns:
	If folders exist, returns a list of Drive file instance of these folders.
	Otherwise, returns [].
	'''
        files = self.driver.files(title=folder_name)
        files = filter(
          lambda x: x["mimeType"] == "application/vnd.google-apps.folder"
            and (not "explicitlyTrashed" in x or not x["explicitlyTrashed"]) 
	    and "webViewLink" in x,
          files)
        return files

    def create_publish_folder(self, folder_name="publish_folder"):
        '''Create a public folder for uploading files to be published.
        Args:
	folder_name: name of the public folder.

	Returns:
        Driver files instance for the created folder.  
	The folder has mimeType 'application/vnd.google-apps.folder'.
	'''
        import thedriver
        if self.driver.service==None:
            self.driver.build()
        body = { 
		"title": folder_name, 
		"mimeType": "application/vnd.google-apps.folder"
	       }
        file = service.files().insert(body=body).execute()
        permission = {
                      "value": "",
                      "type": "anyone",
                      "role": "reader"
                     }
        
        service.permissions().insert(
        fileId=file["id"], body=permission).execute()
        return file
        
    def upload_html(self, filename):
        '''Upload a local html file to publish_folder.
	Args:
	filename: path to the file to upload.
       
        Returns:
	Drive File instance for the uploaded file.
	'''
        media_body = MediaFileUpload(filename, mimetype="text/html", resumable=True)
	body = {
           "title": filename,
           "description": "a html file uploaded by thedriver",
	   "mimeType": "text/html",
	   "parents": [{
		   "kind":"drive#fileLink",
		   "id":self.uploadFolder["id"]
		   }]
	   }
	file = self.driver.service.files().insert(body=body, media_body=media_body).execute()
	print self.uploadFolder["webViewLink"] + filename
	return file 

    def __init__(self, driver=None, folder_name="publish_folder"):
        import thedriver
        if driver == None:
            self.driver = thedriver.go()
	    self.driver.build()
        folders = self.find_publish_folder(folder_name)
	if len(folders) == 0:
		create_publish_folder(folder_name)
		folders = self.find_publish_folder(folder_name)
        self.uploadFolder = folders[0]

