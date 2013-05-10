#!/usr/bin/python

import httplib2
import pprint

from apiclient.discovery import build
from apiclient.http import MediaFileUpload
from oauth2client.client import OAuth2WebServerFlow


# Copy your credentials from the APIs Console
CLIENT_ID = '225117007438-c93selkie7am9u437rek3ih1fikd51r2.apps.googleusercontent.com'
CLIENT_SECRET = 'Qih7X5Ssa3Wu0Tcfw5p5tpen'
#oauth_code = '4/ZxKaQ29rHgLBxwgVDgZCdIMIEVwB.MmgIWm-PIa8QuJJVnL49Cc_Euj4gfQI'
oauth_code = ""

# Path to the file to upload
FILENAME = 'document.txt'

# Check https://developers.google.com/drive/scopes for all available scopes
OAUTH_SCOPE = 'https://www.googleapis.com/auth/drive'

# Redirect URI for installed apps
REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'

flow = OAuth2WebServerFlow(CLIENT_ID, CLIENT_SECRET, OAUTH_SCOPE, REDIRECT_URI)
if not oauth_code:
  # Run through the OAuth flow and retrieve credentials
  authorize_url = flow.step1_get_authorize_url()
  print 'Go to the following link in your browser: ' + authorize_url
  oauth_code = raw_input('Enter verification code: ').strip()

credentials = flow.step2_exchange(oauth_code)

# Create an httplib2.Http object and authorize it with our credentials
http = httplib2.Http()
http = credentials.authorize(http)

drive_service = build('drive', 'v2', http=http)

# Insert a file
media_body = MediaFileUpload(FILENAME, mimetype='text/plain', resumable=True)
body = {
  'title': 'My document',
  'description': 'A test document',
  'mimeType': 'text/plain'
}

file = drive_service.files().insert(body=body, media_body=media_body).execute()
pprint.pprint(file)
