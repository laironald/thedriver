#!/usr/bin/python
import os
if os.path.exists("test.db"):
    os.remove("test.db")

import sys
sys.path.append('..')

import unittest
import thedriver
import thedriver.download as drived
import data_interface

config = data_interface.config


class TestTheDriver(unittest.TestCase):
    def setUp(self):
        self.g = thedriver.go()
        #self.f = self.g.files(title="Testing")

    def tearDown(self):
        self.g = None

    def test_download(self):
        filedict = {u'mimeType': u'application/vnd.google-apps.document', u'appDataContents': False, u'thumbnailLink': u'https://docs.google.com/feeds/vt?gd=true&id=1TE0ouM01lsPvot5aZRDv9D7-xC-kLJ0dg3S_zPdWrO4&v=49&s=AMedNnoAAAAAUf9ctF4CHamOIVSI0LEVJjfm7TUsyi0m&sz=s220', u'labels': {u'restricted': False, u'starred': False, u'viewed': True, u'hidden': False, u'trashed': False}, u'etag': u'"RFvxxXV9yoZniidCHgcusodAlXI/MTM3MDY2MzQwNTU0NQ"', u'lastModifyingUserName': u'Ron Lai', u'writersCanShare': True, u'owners': [{u'kind': u'drive#user', u'isAuthenticatedUser': True, u'displayName': u'Driver Jones', u'permissionId': u'11795692365044288237'}], u'id': u'1TE0ouM01lsPvot5aZRDv9D7-xC-kLJ0dg3S_zPdWrO4', u'lastModifyingUser': {u'picture': {u'url': u'https://lh4.googleusercontent.com/-ATIG8Nn0e0w/AAAAAAAAAAI/AAAAAAAADM0/CG4osv4BJao/s64/photo.jpg'}, u'kind': u'drive#user', u'isAuthenticatedUser': False, u'displayName': u'Ron Lai', u'permissionId': u'13081141901108496945'}, u'title': u'Testing', u'ownerNames': [u'Driver Jones'], u'lastViewedByMeDate': u'2013-08-04T15:35:50.928Z', u'parents': [{u'isRoot': True, u'kind': u'drive#parentReference', u'id': u'0AECwzQXjlJkoUk9PVA', u'selfLink': u'https://www.googleapis.com/drive/v2/files/1TE0ouM01lsPvot5aZRDv9D7-xC-kLJ0dg3S_zPdWrO4/parents/0AECwzQXjlJkoUk9PVA', u'parentLink': u'https://www.googleapis.com/drive/v2/files/0AECwzQXjlJkoUk9PVA'}], u'exportLinks': {u'text/html': u'https://docs.google.com/feeds/download/documents/export/Export?id=1TE0ouM01lsPvot5aZRDv9D7-xC-kLJ0dg3S_zPdWrO4&exportFormat=html', u'application/pdf': u'https://docs.google.com/feeds/download/documents/export/Export?id=1TE0ouM01lsPvot5aZRDv9D7-xC-kLJ0dg3S_zPdWrO4&exportFormat=pdf', u'application/vnd.openxmlformats-officedocument.wordprocessingml.document': u'https://docs.google.com/feeds/download/documents/export/Export?id=1TE0ouM01lsPvot5aZRDv9D7-xC-kLJ0dg3S_zPdWrO4&exportFormat=docx', u'application/vnd.oasis.opendocument.text': u'https://docs.google.com/feeds/download/documents/export/Export?id=1TE0ouM01lsPvot5aZRDv9D7-xC-kLJ0dg3S_zPdWrO4&exportFormat=odt', u'application/rtf': u'https://docs.google.com/feeds/download/documents/export/Export?id=1TE0ouM01lsPvot5aZRDv9D7-xC-kLJ0dg3S_zPdWrO4&exportFormat=rtf', u'text/plain': u'https://docs.google.com/feeds/download/documents/export/Export?id=1TE0ouM01lsPvot5aZRDv9D7-xC-kLJ0dg3S_zPdWrO4&exportFormat=txt'}, u'shared': True, u'editable': True, u'kind': u'drive#file', u'modifiedDate': u'2013-06-08T03:50:05.545Z', u'createdDate': u'2013-05-11T17:03:57.988Z', u'iconLink': u'https://ssl.gstatic.com/docs/doclist/images/icon_11_document_list.png', u'embedLink': u'https://docs.google.com/document/d/1TE0ouM01lsPvot5aZRDv9D7-xC-kLJ0dg3S_zPdWrO4/preview', u'alternateLink': u'https://docs.google.com/document/d/1TE0ouM01lsPvot5aZRDv9D7-xC-kLJ0dg3S_zPdWrO4/edit?usp=drivesdk', u'copyable': True, u'modifiedByMeDate': u'2013-06-05T18:23:16.709Z', u'userPermission': {u'kind': u'drive#permission', u'etag': u'"RFvxxXV9yoZniidCHgcusodAlXI/AJJVj8jO_bOEG3udOPHXbjVVFag"', u'role': u'owner', u'type': u'user', u'id': u'me', u'selfLink': u'https://www.googleapis.com/drive/v2/files/1TE0ouM01lsPvot5aZRDv9D7-xC-kLJ0dg3S_zPdWrO4/permissions/me'}, u'quotaBytesUsed': u'0', u'selfLink': u'https://www.googleapis.com/drive/v2/files/1TE0ouM01lsPvot5aZRDv9D7-xC-kLJ0dg3S_zPdWrO4'}
        content = drived.download(self.g, filedict)
        self.assertTrue("<html>" in content)

    # --- FORMAT CLASS ---
    def test_format_init(self):
        self.assertTrue("<html>" in drived.format('document.html').html)
        self.assertEqual(drived.format("content").html, "content")


if __name__ == '__main__':
    unittest.main()
