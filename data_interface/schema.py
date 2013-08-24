from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text
from sqlalchemy import DateTime
from sqlalchemy.orm import relationship, backref
from sqlalchemy import func


''' +++++++++++++++++++++++++++++++++++
Define Tables:
+++++++++++++++++++++++++++++++++++ '''

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(45), unique=True)
    handle = Column(String(45), unique=True)
    google_account = Column(String(45))
    oauth_code = Column(String(45))
    email = Column(String(45))
    time_created = Column(DateTime, default=func.now())
    time_updated = Column(DateTime, default=func.now(), onupdate=func.now())

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
    alternateLink = Column(String(256))
    htmlLink = Column(String(256))
    html = Column(Text)  # compiled html
    time_created = Column(DateTime, default=func.now())
    time_updated = Column(DateTime, default=func.now(), onupdate=func.now())

    user_id = Column(Integer, ForeignKey('user.id'))
    folder_id = Column(Integer, ForeignKey('folder.id'))


class Folder(Base):
    __tablename__ = 'folder'

    id = Column(Integer, primary_key=True)
    name = Column(String(45))
    is_root = Column(Boolean)
    time_created = Column(DateTime, default=func.now())
    time_updated = Column(DateTime, default=func.now(), onupdate=func.now())

    user_id = Column(Integer, ForeignKey('user.id'))
    parent_folder_id = Column(Integer, ForeignKey('folder.id'))

    document = relationship("Document", backref="folder")
    child_folder = relationship("Folder", backref=backref("parent_folder", remote_side=[id]))

''' +++++++++++++++++++++++++++++++++++++++++++++
End of define.
+++++++++++++++++++++++++++++++++++++++++++++ '''
