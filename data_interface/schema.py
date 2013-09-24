from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text
from sqlalchemy import DateTime
from sqlalchemy.orm import relationship, backref
from sqlalchemy import func
from unidecode import unidecode


''' +++++++++++++++++++++++++++++++++++
Define Tables:
 * Likely +analytic table at some point?
   (or should this be all managed by )

 These fields are pesistent in every database:
 * time_created: the time the entry was created
 * time_updated: the time that the entry was updated
+++++++++++++++++++++++++++++++++++ '''

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    """
    name: the fullname of the user
    handle: the hanle of the user (ie. @liwen)
    google_account: ?
    oauth_code: <is this sufficient for auth?>
    email: the email address of the user
    """

    id = Column(Integer, primary_key=True)
    name = Column(String(45), unique=True)
    handle = Column(String(45), unique=True)
    google_account = Column(String(45))
    credentials = Column(String(45))
    email = Column(String(45))
    time_created = Column(DateTime, default=func.now())
    time_updated = Column(DateTime, default=func.now(), onupdate=func.now())

    document = relationship("Document", backref="user")
    folder = relationship("Folder", backref="user")

    def __repr__(self):
        return "<User('{0}')>".format(unidecode(self.name))


class Document(Base):
    """
    name: the title of the document
    googledoc_id: google document identifier
    password: a special password for the document (if protected)
    handle: the handle of a document (ie. @testing)
    is_protected: specifies whether the doc is protected
    is_published: ??
    alternateLink: url for google iframe
    htmlLink: document exported as html
    html: post published generated html
    share_status
        0 = public
        1 = unlisted
        2 = private
    time_opened: last time the owner opened the document

    note: we are currently assuming
        user>document, n>1 relationship
    """
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
    share_status = Column(Integer, default=0)
    time_created = Column(DateTime, default=func.now())
    time_updated = Column(DateTime, default=func.now(), onupdate=func.now())
    time_opened = Column(DateTime, default=func.now())

    user_id = Column(Integer, ForeignKey('user.id'))
    folder_id = Column(Integer, ForeignKey('folder.id'))

    def __repr__(self):
        return "<Document('{0}')>".format(unidecode(self.name))


class Folder(Base):
    __tablename__ = 'folder'
    """
    name: ??? name of the folder name?
    is_root: ???
    """

    id = Column(Integer, primary_key=True)
    name = Column(String(45))
    is_root = Column(Boolean)
    time_created = Column(DateTime, default=func.now())
    time_updated = Column(DateTime, default=func.now(), onupdate=func.now())

    user_id = Column(Integer, ForeignKey('user.id'))
    parent_folder_id = Column(Integer, ForeignKey('folder.id'))

    document = relationship("Document", backref="folder")
    child_folder = relationship("Folder", backref=backref("parent_folder", remote_side=[id]))

    def __repr__(self):
        return "<Folder('{0}')>".format(unidecode(self.name))


''' +++++++++++++++++++++++++++++++++++++++++++++
End of define.
+++++++++++++++++++++++++++++++++++++++++++++ '''
