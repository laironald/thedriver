from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.sql import exists

''' +++++++++++++++++++++++++++++++++++
Set Configuration:
+++++++++++++++++++++++++++++++++++ '''


def get_config(localfile="config.ini", default_file=True):
    """
    This grabs a configuration file and converts it into
    a dictionary.

    The default filename is called config.ini
    First we load the global file, then we load a local file
    """
    import os
    import re
    import ConfigParser
    from collections import defaultdict

    if default_file:
        openfile = "{0}/config.ini".format(os.path.dirname(os.path.realpath(__file__)))
    else:
        openfile = localfile
    config = defaultdict(dict)
    if os.path.isfile(openfile):
        cfg = ConfigParser.ConfigParser()
        cfg.read(openfile)
        for s in cfg.sections():
            for k, v in cfg.items(s):
                dec = re.compile('\d+(\.\d+)?')
                if v in ("True", "False") or v.isdigit() or dec.match(v):
                    v = eval(v)
                config[s][k] = v

    # this enables us to load a local file
    if default_file:
        newconfig = get_config(localfile, default_file=False)
        for section in newconfig:
            for item in newconfig[section]:
                config[section][item] = newconfig[section][item]

    return config

config = get_config()

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
    child_folder = relationship("Folder", backref=backref("parent_folder", remote_side=[id]))

''' +++++++++++++++++++++++++++++++++++++++++++++
End of define.
+++++++++++++++++++++++++++++++++++++++++++++ '''


class GhostDBConnector():
    engine = None
    session = None

    def __init__(self):
        echo = config.get("global").get("echo")
        database = config.get("global").get("database")
        if database == "mysql":
            self.engine = create_engine('mysql://{user}:{password}@{host}:3306/{database}'.format(**config.get(database)), echo=echo, pool_recycle=3600)
        else:
            self.engine = create_engine('sqlite:///{path}/{database}'.format(**config.get(database)), echo=echo)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        self.CreateDB()

    def CreateDB(self):
        ''' Create tables as defined above

        '''
        Base.metadata.create_all(self.engine, checkfirst=True)

    def add_user(self, arg_name, arg_google_account, arg_oauth_code):
        ''' Add a new user to GhostDocs

        '''
        user = User(name=arg_name,
                    google_account=arg_google_account,
                    oauth_code=arg_oauth_code)
        self.session.add(user)
        self.session.commit()

    def add_doc(self, file, user_id):
        ''' import a google doc into GhostDocs
        Args:
            file: metadata of a google doc
        Returns:
            return 0 if add doc sucessfully;
            return -1 if doc already added to GhostDocs.
        '''
        if self.doc_exists(file['id']):
            return -1

        doc = Document(name=file['title'],
                       googledoc_id=file['id'],
                       alternateLink=file['alternateLink'],
                       is_published=False,
                       user_id=user_id)

        self.session.add(doc)
        self.session.commit()

        return 0

    def update_doc(self, arg_googledoc_id, html):
        ''' update a published doc
        Args:
            arg_googledoc_id: id of a google doc
            html: compiled HTML

        Returns:
            return 0 if update sucessfully;
            return -1 if doc does not exist in GhostDocs;
        '''
        doc = self.find_doc(arg_googledoc_id).first()
        if not doc:
            return -1
        doc.html = html
        doc.is_published = True
        self.session.commit()
        return 0

    def doc_exists(self, arg_googledoc_id):
        flag = self.session.query(exists().where(Document.googledoc_id == arg_googledoc_id)).scalar()
        return flag

    def find_doc(self, arg_googledoc_id):
        docs = self.session.query(Document).filter(Document.googledoc_id == arg_googledoc_id)
        return docs

    def list_ghost_docs(self, user_id):
        docs = self.session.query(Document).filter(Document.user_id == user_id).all()
        return docs

    def find_doc_by_user(self, username, dochandle):
        # TODO: might want to use join logic. maybe.
        user = self.session.query(User).filter(User.handle == username)
        if user.count():
            for doc in user.first().document:
                if doc.handle == dochandle:
                    return doc


def sample_run():
    connector = GhostDBConnector()
    connector.CreateDB()
    user = User(**config.get("drive"))
    connector.session.add(user)
    connector.session.commit()
