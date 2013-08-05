import ghost_db
import thedriver
import thedriver.download as drived


db_connector = ghost_db.GhostDBConnector()
config = ghost_db.get_config()
gdoc_mimeType = config.get("global").get("gdoc_mimeType")


class UserSession:
    drive = None
    user_id = None  # ghost doc id
    name = None  # ghost doc username

    def __init__(self, user_name=None):
        self.name = user_name
        self.drive = thedriver.go()
        self.drive.build()

user_session = UserSession()


# --------------------------------


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


def list_google_docs(user_id=None, if_hide_ghost_doc=True):
    """list a user's all editable google docs

    Args:
        user_id: user's GhostDocs id
        if_hide_ghost_doc: if remove docs already exist in ghost docs from the list

    Returns:
        A list of metadata of editable google docs.
        examples:
        [ {u'mimeType':u'application/vnd.google-apps.document',
          u'title':u'Test' ... },
          {...}
        ]

    """
    files = user_session.drive.files()
    google_docs = filter(lambda f: f['mimeType'] == gdoc_mimeType
                         and (not 'explicitlyTrashed' in f
                         or not f['explicitlyTrashed'])
                         and f['editable'], files)
    return google_docs


def list_recent_docs(user_id):
    pass


def load_doc(user_id=None, google_doc_id=None):
    """
    return the meta data of a google doc. (the 'alternateLink' is used for embedding the iframe.

    Warning:  the default arg values user_id=None and google_doc_id=None are both for ease of testing.

    Args:
        user_id: GhostDoc user_id
        google_doc_id: id of the google doc

    Returns:
        meta data of a google doc.
    """
    if not user_id:  # remove this condition (it's only for testing)
        user_id = 1

    if google_doc_id:
        filedict = user_session.drive.service.files().get(fileId=google_doc_id).execute()
    else:  # TODO remove this else branch. (this else branch is only for testing)
        #file = user_session.drive.files(title="test")[0];
        filedict = list_google_docs()[0]
        google_doc_id = filedict['id']
    if not db_connector.doc_exists(google_doc_id):
        db_connector.add_doc(filedict, user_id)
    return filedict


def add_user(user_name, google_account, oauth_code):
    """
    register a new GhostDocs user
    """
    user = ghost_db.User(name=user_name,
                         google_account=google_account,
                         oauth_code=oauth_code)
    db_connector.session.add(user)
    db_connector.session.commit()


def preview_doc(user_id=None, filedict=None):
    """
    process a google doc and show the compiled HTML.
    Warning:  the default arg values user_id=None and google_doc_id=None are both for ease of testing.

    Args:
        user_id: GhostDoc user_id.
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
    if not filedict:
        filedict = list_google_docs()[0]

    doc_in_html = drived.download(user_session.drive, filedict)
    out = drived.format(doc_in_html)
    out.remove_comments()
    return out.html


def publish_doc(user_id=None, filedict=None):
    """
    Process a google doc and publish it.

    Warning:  the default arg values user_id=None and google_doc_id=None are both for ease of testing.

    Args:
        user_id: GhostDoc user_id.
        file: metadata of a google doc.

    Returns:
        Compiled HTML as a string.
    """
    if not filedict:
        filedict = list_google_docs()[0]

    html_compiled = preview_doc(user_id, filedict)
    if not db_connector.doc_exist(arg_google_doc_id):
        db_connector.add_doc(filedict, 123)
    db_connector.update_doc(filedict['id'], html_compiled)

    return html_compiled


def view_doc(user_id=None, arg_google_doc_id=None):
    """
    Load the content of a compiled doc.

    Warning:  the default arg values user_id=None and google_doc_id=None are both for ease of testing.

    Args:
        user_id: GhostDoc user_id.
        google_doc_id: id of a google doc.

    Returns:
        HTML as a string. ( need to return more, such as navigation. )
    """
    if not arg_google_doc_id:
        arg_google_doc_id = list_google_docs()[0]['id']

    doc = db_connector.find_doc(arg_google_doc_id)[0]
    html = doc.html
    return html
