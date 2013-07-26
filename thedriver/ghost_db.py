from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, backref

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


class GhostDBConnector():
        engine = None
        session = None
        def __init__(self):
                self.engine = create_engine('mysql://liwen:liwen123@mysql.goideas.org:3306/thedriver', 
                                echo=True)
                Session = sessionmaker(bind=self.engine)
                self.session = Session()

        def CreateDB(self):
                Base.metadata.create_all(self.engine);


def sample_run():
        connector = GhostDBConnector()
        connector.CreateDB()
