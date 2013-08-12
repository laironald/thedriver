#!/usr/bin/python
import sys
import unittest
sys.path.append('..')

import data_interface as di 
import data_interface.ghost_db as db
from sqlalchemy.sql import exists

class TestDataInterface(unittest.TestCase):
    def setUp(self):
        ''' the tests are informal.  because: profiles of a user e.g. google_account, oauth_code, user_id, etc.  are hard-coded.
        '''

        # add one user to database
        self.user = { 
                     'user_name':'jones',
                     'google_account':'thedriverjones',
                     'oauth_code':'somecode'}
        if not di.db_connector.session().query(exists().where(db.User.name == 'jones')).scalar():
                di.add_user(**self.user)
                pass
        self.user['id'] = di.db_connector.session().query(db.User).filter(db.User.name=='jones').first().id

        file = di.list_google_docs()[0]
        di.load_doc(self.user['id']) # this adds one doc to the database

        
    def tearDown(self):
        pass

    def test___init__(self):
        self.assertEqual(1, 1)
        self.assertItemsEqual([1,2],[2,1])
        self.assertIn(1, [1,2])

    def test_list_google_docs(self):
        # test: list google docs
        files = di.list_google_docs(self.user['id'])
        self.assertTrue( len(files)>0 )

    def test_list_ghost_docs(self):
        # test: list ghost docs
        files = di.list_ghost_docs(self.user['id'])
        self.assertTrue( len(files)>0 )

    def test_load_doc(self):
        files = di.list_google_docs() 
        file=di.load_doc(self.user['id'],files[0]['id'])
        self.assertTrue( 'alternateLink' in file )

    def test_preview_doc(self):
        file=di.list_google_docs()[0]
        compiled_html = di.preview_doc(self.user['id'],file)
        self.assertTrue( len(compiled_html)>0 ) 

    def test_publish_doc(self):
        file = di.list_google_docs()[0]
        compiled_html = di.publish_doc(self.user['id'], file)
        self.assertTrue( len(compiled_html)>0 )


if __name__ == '__main__':
    unittest.main()

