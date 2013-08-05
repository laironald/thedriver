import ghost_db
import thedriver
import thedriver.download as drived

db_connector = ghost_db.GhostDBConnector()
config = ghost_db.get_config()
gdoc_mimeType = config.get("global").get("gdoc_mimeType")


class UserSession:
    drive = None
    name = None  # ghost doc username

    def __init__(self, user_name=None):
        self.name = user_name
        self.drive = thedriver.go()
        self.drive.build()


def check_auth(user_id):
    """
    # TODO
    Let's create a way to check that a user is actually
    authenticated!
    """

def list_ghost_docs(user_id):
    '''
    # TODO
    '''
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
    files = session.drive.files()
    google_docs = filter(lambda f: f['mimeType'] == gdoc_mimeType
                         and (not 'explicitlyTrashed' in f
                         or not f['explicitlyTrashed'])
                         and f['editable'], files)
    return google_docs


def list_recent_docs(user_id):
    pass


def load_doc(user_id=None, google_doc_id=None):
    '''return the meta data of a google doc. (the 'alternateLink' is used for embedding the iframe.

    Warning:  the default arg values user_id=None and google_doc_id=None are both for ease of testing.

    Args:
        user_id: GhostDoc user_id
        google_doc_id: id of the google doc

    Returns:
        meta data of a google doc.
    '''

    if google_doc_id:
        file = session.drive.service.files().get(fileId=google_doc_id).execute()
    else:  # TODO remove this else branch. (this else branch is only for testing)
        file = session.drive.files(title="test")[0]
    return file


def add_user(user_name, google_account, oauth_code):
    user = ghost_db.User(name=user_name,
                         google_account=google_account,
                         oauth_code=oauth_code)
    db_connector.session.add(user)
    db_connector.session.commit()


def preview_doc(user_id=None, file=None):
    ''' process a google doc and show the compiled HTML.
    Warning:  the default arg values user_id=None and google_doc_id=None are both for ease of testing.

    Args:
        user_id: GhostDoc user_id.
        file: metadata of a google doc.

    Returns:
        HTML as a string.

    '''

    '''
    if google_doc_id:
        file = session.drive.service.files().get(fileId=google_doc_id).execute()
    else:  # TODO remove this else branch. (this else branch is only for testing)
        file = session.drive.files(title="test")[0];
    '''
    if not file:
        file = session.drive.files(title="test")[0]

    doc_in_html = drived.download(session.drive, file)
    out = drived.format(doc_in_html)
    out.remove_comments()
    return out.html


def publish_doc(user_id=None, file=None):
    ''' Process a google doc and publish it.

    Warning:  the default arg values user_id=None and google_doc_id=None are both for ease of testing.

    Args:
        user_id: GhostDoc user_id.
        file: metadata of a google doc.

    Returns:
        Compiled HTML as a string.
    '''
    if not file:
        file = session.drive.files(title="test")[0]

    html_compiled = preview_doc(user_id, file)
    if not db_connector.doc_exist(arg_google_doc_id):
        connector.add_doc(file, 123)

    connector.update_doc(file['id'], html_compiled)

    return html_compiled


def view_doc(user_id=None, arg_google_doc_id=None):
    ''' Load the content of a compiled doc.

    Warning:  the default arg values user_id=None and google_doc_id=None are both for ease of testing.

    Args:
        user_id: GhostDoc user_id.
        google_doc_id: id of a google doc.

    Returns:
        HTML as a string. ( need to return more, such as navigation. )
    '''
    if not arg_google_doc_id:
            arg_google_doc_id = list_google_docs()[0]['id']

    doc = db_connector.find_doc(arg_google_doc_id)[0]
    html = doc.html
    return html


session = UserSession()
