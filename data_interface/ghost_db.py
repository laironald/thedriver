from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import exists
from schema import *
from datetime import datetime

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


# -------------------------------------------


class GhostDBConnector():
    engine = None
    _session = None
    echo = None
    database = None

    def __init__(self):
        self.echo = config.get("global").get("echo")
        self.database = config.get("global").get("database")
        self.refresh_connection()
        self.CreateDB()

    def commit(self):
        """
        Convenience method to call commit
        """
        self.session().commit()

    def session(self):
        try:
            self._session.execute('select 1')
        except:
            print 'refreshing connection'
            self.refresh_connection()
        return self._session

    def refresh_connection(self):
        if self.database == "mysql":
            self.engine = create_engine('mysql://{user}:{password}@{host}:3306/{database}'.format(**config.get(self.database)), echo=self.echo, pool_recycle=3600)
        else:
            self.engine = create_engine('sqlite:///{path}/{database}'.format(**config.get(self.database)), echo=self.echo)
        Session = sessionmaker(bind=self.engine)
        self._session = Session()

    def CreateDB(self):
        ''' Create tables as defined above

        '''
        Base.metadata.create_all(self.engine, checkfirst=True)

    def get_credentials(self, userhandle):
        user = self.session().query(User).filter(User.handle == userhandle).first()
        return user.credentials


    def add_user(self, arg_name, arg_google_account, arg_credentials):
        ''' Add a new user to GhostDocs

        '''
        user = User(name=arg_name,
                    google_account=arg_google_account,
                    credentials=arg_credentials)
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

        self.session().add(doc)
        self.session().commit()

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
        self.session().commit()
        return 0

    def doc_exists(self, arg_googledoc_id):
        """ This checks if a google doc has ever been imported.
        Args:
            arg_googledoc_id: id of a google doc

        Returns:
            returns 0 if doc doesn't exists in ghostdocs' d/b.
            returns 1 if positive.
        """
        flag = self.session().query(exists().where(Document.googledoc_id == arg_googledoc_id)).scalar()
        return flag

    def find_doc(self, arg_googledoc_id):
        """ This finds documents with the given id.

        Args:
            arg_googledoc_id: id of a google doc.

        Returns:
            a list of Document instances.

        """
        docs = self.session().query(Document).filter(Document.googledoc_id == arg_googledoc_id)
        return docs

    def find_google_user(self, arg_google_account):
        """ Find a GhostDocs user by google account.

        Args:
            arg_google_account: google account.  e.g.  thedriverjones

        Returns:
            A User instance.
        """
        user = self.session().query(User).filter(User.google_account == arg_google_account)
        if user.count(): 
            return user.first()
        else:
            return None

    def find_ghostdocs_user(self, arg_userhandle):
        """ Find a GhostDocs user by handle.

        Args:
            arg_userhandle: google account.  e.g.  thedriverjones

        Returns:
            A User instance.
        """
        user = self.session().query(User).filter(User.handle == arg_userhandle)
        if user.count(): 
            return user.first()
        else:
            return None

    def list_ghost_docs(self, user_id):
        ''' list a user's ghostdocs files

        Args:
            user_id: user's ghostdocs id.

        Return:
            a list of Document instances.

        '''
        user = self.session().query(User).filter(User.handle == user_id).first()
        return user.document

    def find_doc_by_user(self, username, dochandle):
        # TODO: might want to use join logic. maybe.
        user = self.session().query(User).filter(User.handle == username)
        if user.count():
            for doc in user.first().document:
                if doc.handle == dochandle:
                    return doc


def sample_run():
    ''' not in user anymore.  ignore this. '''
    connector = GhostDBConnector()
    connector.CreateDB()
    user = User(**config.get("drive"))
    connector.session.add(user)
    connector.session.commit()
