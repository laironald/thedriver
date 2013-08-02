from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, Boolean, ForeignKey, Text
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.sql import exists

''' +++++++++++++++++++++++++++++++++++
Define Tables:
+++++++++++++++++++++++++++++++++++ '''

Base = declarative_base()

class User(Base):
        __tablename__ = 'user'

        id = Column(Integer, primary_key=True)
        name = Column(String(45))
        handle = Column(String(45))
        google_account = Column(String(45))
        oauth_code = Column(String(45))

        document = relationship("Document", backref="user")
        folder = relationship("Folder", backref="user")

class Document(Base):
        __tablename__ = 'document'

        id = Column(Integer, primary_key=True)
        name = Column(String(45))
        googledoc_id = Column(String(45))
        password = Column(String(45))
        handle = Column(String(45))
        is_protected = Column(Boolean)
        is_published = Column(Boolean)
        alternateLink = Column(String(45))
        html = Column(Text) # compiled html

        user_id = Column(Integer, ForeignKey('user.id'))
        folder_id = Column(Integer, ForeignKey('folder.id'))

class Folder(Base):
        __tablename__ = 'folder'

        id = Column(Integer, primary_key=True)
        name = Column(String(45))
        is_root = Column(Boolean)

        user_id = Column(Integer, ForeignKey('user.id'))
        parent_folder_id = Column(Integer, ForeignKey('folder.id'))

        document = relationship("Document", backref="folder")
        child_folder = relationship("Folder", backref=backref("parent_folder",remote_side=[id]))

''' +++++++++++++++++++++++++++++++++++++++++++++
End of define.
+++++++++++++++++++++++++++++++++++++++++++++ '''


class GhostDBConnector():
        engine = None
        session = None
        def __init__(self):
                self.engine = create_engine('mysql://liwen:liwen123@mysql.goideas.org:3306/thedriver', 
                                echo=True)
                Session = sessionmaker(bind=self.engine)
                self.session = Session()

        def CreateDB(self):
                ''' Create tables as defined above

                '''
                Base.metadata.create_all(self.engine);

        def add_user( self, arg_name, arg_google_account, arg_oauth_code ):
                user = User(name=arg_name, 
                            google_account=arg_google_account,
                            oauth_code=arg_oauth_code);
                self.session.add(user);
                self.session.commit();

        def add_doc( self, file, user_id ):
                ''' import a google doc into GhostDocs
                Args:
                    file: metadata of a google doc
                Returns: 
                    return 0 if add doc sucessfully;
                    return -1 if doc already added to GhostDocs.
                '''
                # TODO  link file with a user
                if self.doc_exists( file['id']):
                        return -1

                doc = Document(name=file['title'], 
                               googledoc_id=file['id'], 
                               alternateLink=file['alternateLink'],
                               is_published=False)
                self.session.add(doc);
                self.session.commit();

                return 0

        def update_doc( self, arg_googledoc_id, html):
                ''' update a published doc
                Args:
                    arg_googledoc_id: id of a google doc
                    html: compiled HTML

                Returns:
                    return 0 if update sucessfully;
                    return -1 if doc does not exist in GhostDocs;
                '''
                doc = self.find_doc( arg_googledoc_id ).first()
                if not doc:
                        return -1
                doc.html = html
                doc.is_published = True
                self.session.commit()


                return 0

        def doc_exists( self, arg_googledoc_id ):
                flag = self.session.query(exists().where(Document.googledoc_id==arg_googledoc_id)).scalar() 

                return flag

        def find_doc( self, arg_googledoc_id ):
                docs = self.session.query(Document).filter_by(googledoc_id=arg_googledoc_id)
                return docs


def sample_run():
        connector = GhostDBConnector()
        connector.CreateDB()
        user = User(name='jones',
                        google_account='thedriverjones',
                        oauth_code=u'someoauthcodeforaccessingjonesgoogledrive')
        connector.session.add(user)
        connector.session.commit()

