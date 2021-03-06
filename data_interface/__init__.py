import ghost_db
import thedriver
import thedriver.download as drived
import pickle
from datetime import datetime


db_connector = ghost_db.GhostDBConnector()
config = ghost_db.get_config()
gdoc_mimeType = config.get("global").get("gdoc_mimetype")


class UserSession:
    drive = None
    user_id = None  # ghost doc id (abandon this and use username as id?)
    username = None  # ghost doc username

    def __init__(self, userhandle=None):
        if not userhandle:
            userhandle = 'ghostie'
        self.username = userhandle
        cred = db_connector.get_credentials(userhandle)
        cred = pickle.loads(cred)
        self.drive = thedriver.go(cred)

active_users = {} # a dictionary of current active users

def user_session(userhandle):
    if not userhandle in active_users:
        active_users[userhandle] = UserSession(userhandle)
    return active_users[userhandle] 

# --------------------------------

def fetch_doc_by_id(username, doc_id):
    """
    Return a document by the doc_id
    Also requires the username so we fetch the right one
        (in case there is a duplicate doc that exists)
    """
    for doc in db_connector.session().query(ghost_db.Document).filter(ghost_db.Document.googledoc_id == doc_id):
        if doc.user.handle == username:
            return doc


def fetch_user_doc(browser_session):
    user = db_connector.session().query(ghost_db.User).filter(ghost_db.User.handle == browser_session["user"]).first()
    for doc in user.document:
        if doc.handle == session["doc"]:
            break
    return user, doc


def list_ghost_docs(user_id):
    """ list a user's GhostDocs files

    Args:
        user_id: user's GhostDocs id

    Return:
        a list of Document instances. e.g.:
        [ {id:1, name:'Test', googledoc_id:'FAPI3C9A', password:None, handle:'Jones', is_protected:False, ... },
          {id:2, name:'...', .....  }
        ]
    """
    docs = db_connector.list_ghost_docs(user_id)
    return docs


def check_auth(user_id):
    """
    We probably need a routine that more or less makes
    sure a user is logged online. This could be a decorator?
    If the user is not... we basically reject the action.
    """
    pass


def add_doc(user, new_doc):
    """
    If document already exists, don't add it
    """
    for doc in user.document:
        if doc.googledoc_id == new_doc["id"]:
            return False

    print new_doc
    doc = ghost_db.Document(**{
        "name": new_doc["title"],
        "googledoc_id": new_doc["id"],
        "handle": new_doc["id"],
        "alternateLink": new_doc["alternateLink"],
        "htmlLink": new_doc["exportLinks"]["text/html"]
    })
    user.document.append(doc)
    print 'appending doc ' + doc.name
    db_connector.commit()
    return True


def update_doc_open(doc):
    """
    Update when the last time a document was open
    """
    doc.time_opened = datetime.now()
    db_connector.commit()


def update_doc_meta(doc, meta):
    """
    Update meta data of document
    """
    doc.handle = meta["handle"]
    doc.name = meta["title"]


def list_google_docs(userhandle, if_hide_ghost_doc=True):
    """list a user's all editable google docs

    Args:
        userhandle: user's GhostDocs handle
        if_hide_ghost_doc: if remove docs already exist in ghost docs from the list

    Returns:
        A list of metadata of editable google docs.
        examples:
        [ {u'mimeType':u'application/vnd.google-apps.document',
          u'title':u'Test' ... },
          {...}
        ]
    """
    print '*******listing google docs for ' + userhandle + '**************'
    files = user_session(userhandle).drive.files()
    google_docs = filter(lambda f: f['mimeType'] == gdoc_mimeType
                         and (not 'explicitlyTrashed' in f
                         or not f['explicitlyTrashed'])
                         and f['editable'], files)
    print [x['title'] for x in google_docs] 
    return google_docs


def list_recent_docs(doc, number=10):
    """
    Return a list of documents that were recently opened

    Args:
        user: user that we want to check the docs of
        doc: document we would like to ignore
        number: the maximum number of documents to show
    """
    # research @ relationships where things are auto-sorted
    # is this possible?
    user = doc.user
    docs = sorted(user.document, key=lambda doc: doc.time_opened, reverse=True)
    if doc:
        docs.pop(docs.index(doc))
    return docs[:number]
    pass


def load_doc(username=None, dochandle=None, googledoc_id=None):
    if username and dochandle:
        return db_connector.find_doc_by_user(username, dochandle)
    elif googledoc_id:
        return db_connector.find_doc(googledoc_id)


def create_user(user_name, google_account, user_handle, cred):
    """
    register a new GhostDocs user
    """
    user = ghost_db.User(name=user_name,
                         google_account=google_account,
                         handle=user_handle,
                         credentials=cred)
    db_connector.session().add(user)
    db_connector.session().commit()
    print '[data_interface/create_user()]: new ghostdocs user created! user_handle = ' + user_handle

def find_google_user(google_username):
    """ Find a GhostDocs users by google account.

    Args:
        google_username: google account.  e.g. thedriverjones

    Returns:
        A User instance.
    """
    user = db_connector.find_google_user(google_username)
    return user

def find_ghostdocs_user(userhandle):
    """ Find a GhostDocs users by user handle.

    Returns:
        A User instance.
    """
    user = db_connector.find_ghostdocs_user(userhandle)
    print '*****found ghostdocs user ,  user = ' + user.name + '**********'
    return user


def preview_doc(userhandle, filedict):
    """
    process a google doc and show the compiled HTML.

    Args:
        userhandle: GhostDoc userhandle.
        file: metadata of a google doc.

    Returns:
        HTML as a string.
    """

    """
    if google_doc_id:
        file = user_session.drive.service.files().get(fileId=google_doc_id).execute()
    else:  # TODO remove this else branch. (this else branch is only for testing)
        file = user_session.drive.files(title="test")[0];
    """
    #if not filedict:
    #    filedict = list_google_docs()[0]

    doc_in_html = drived.download(user_session(userhandle).drive, filedict)
    out = drived.format(doc_in_html)
    out.remove_comments()
    return out.html


def publish_doc(userhandle, filedict):
    """
    Process a google doc and publish it.

    Args:
        userhandle: GhostDoc userhandle.
        filedict: metadata of a google doc.

    Returns:
        Compiled HTML as a string.
    """
    if type(filedict).__name__ == "dict":
        if not filedict:
            filedict = list_google_docs()[0]
        # if we want to have a ghostdocs id, this might not
        # be suffice. it probably is in this case
        #  user_id and the doc_id

        # probably need to revisit this in some capacity
        if not db_connector.doc_exist(filedict):
            db_connector.add_doc(filedict, userhandle)
        doc_id = filedict["id"]
        html_compiled = preview_doc(userhandle, filedict)
    else:
        doc = load_doc(googledoc_id=filedict).first()
        doc_id = filedict
        html_compiled = preview_doc(userhandle, doc.htmlLink)

    db_connector.update_doc(doc_id, html_compiled)
    return html_compiled


def view_doc(arg_google_doc_id):
    """
    Load the content of a compiled doc.

    Args:
        user_id: GhostDoc user_id.
        google_doc_id: id of a google doc.

    Returns:
        HTML as a string. ( need to return more, such as navigation. )
    """
    #if not arg_google_doc_id:
    #    arg_google_doc_id = list_google_docs()[0]['id']

    doc = db_connector.find_doc(arg_google_doc_id)[0]
    html = doc.html
    if not html:
        return "No published document"
    else:
        return html
