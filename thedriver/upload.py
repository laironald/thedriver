# this file contains functions for uploading files to google drive

import os
import pickle
import httplib2
import re
import urllib2

from apiclient.http import MediaFileUpload
from apiclient.discovery import build

from apiclient import errors

def retrieve_all_files(service):
    """Retrieve a list of File resources.

    Args:
      service: Drive API service instance.
    Returns:
      List of File resources.
    """
    result = []
    page_token = None
    while True:
        try:
            param = {}
            if page_token:
                param['pageToken'] = page_token
            files = service.files().list(**param).execute()
            result.extend(files['items'])
            page_token = files.get('nextPageToken')
            if not page_token:
                break
        except errors.HttpError, error:
            print 'An error occurred: %s' % error
            break
    return result

def list_files_in_folder(service, folder_id):
  """Print files belonging to a folder.

  Args:
    service: Drive API service instance.
    folder_id: ID of the folder to print files from.
  """
  result = []
  page_token = None
  while True:
    try:
      param = {}
      if page_token:
        param['pageToken'] = page_token
      children = service.children().list(
          folderId=folder_id, **param).execute()

      for child in children.get('items', []):
        result.append(child['id'])
      page_token = children.get('nextPageToken')
      if not page_token:
        break
    except errors.HttpError, error:
      print 'An error occurred: %s' % error
      break
  return result

''' not necessary to set up this function. 
put it here as a reminder of the usage. '''
def get_file_by_id(service, fileId):
    return service.files().get(fileId=fileId).execute()

class uploader():
    driver = None
    uploadFolder = None
    convertTab = {"html": "text/html","txt": "text/plain" }

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
    def get_mimeType(self, filename):
        ext = filename.split(".")[-1]
	return self.convertTab[ext]
        
    def upload(self, filename):
        '''Upload a local file to publish_folder.
	Args:
	filename: path to the file to upload.
       
        Returns:
	Drive File instance for the uploaded file.
	'''
	conflict_files = self.driver.files(title=filename)
	conflict_files = filter(
            lambda f:
	    f["title"] == filename
            and (not "explicitlyTrashed" in f or not f["explicitlyTrashed"]) 
	    and f["parents"] != self.uploadFolder["id"],
          conflict_files)
	if conflict_files:
	    print "uploader.upload: file already exists!"
	    return
	mimeType = self.get_mimeType(filename); 
        media_body = MediaFileUpload(filename, mimetype=mimeType, resumable=True)
	body = {
           "title": filename,
           "description": "a html file uploaded by thedriver",
	   "mimeType": mimeType,
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

