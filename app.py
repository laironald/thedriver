#from flask.ext.assets import Environment, Bundle
#consider Flask-Assets, but sometime later
#https://github.com/Pitmairen/hamlish-jinja

import hamlish_jinja
import json
import random
import string
import httplib2
import pickle
import os

path=os.path.dirname(os.path.realpath(__file__))
os.chdir(path) # change working directory to folder of this app.py

from flask import Flask, render_template
from flask import request, session
from flask import make_response, redirect, url_for
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from oauth2client.client import OAuth2WebServerFlow

import data_interface as di

app = Flask(__name__, static_folder='static', static_url_path='')
app.debug = di.config.get("global").get("app_debug")

app.jinja_env.add_extension(hamlish_jinja.HamlishExtension)
app.jinja_env.hamlish_enable_div_shortcut = True
app.secret_key = di.config.get("global").get("secret")

CLIENT_ID = json.loads(open('client_secrets.json','r').read())['web']['client_id']

# url_for('static', filename='all.css')


@app.route('/')
def index():
    '''Initialize a session for the current user, and render welcome.html.'''
    '''Show log-in botton if user hasn't logged in.'''
    # Create a state token.
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    session['state'] = state
    return render_template('welcome.html', STATE = state, CLIENT_ID=CLIENT_ID)



# --- login callback ---
@app.route('/auth', methods=['POST','GET'])
def callback_handler():
    # Ensure that the request is not a forgery and that the user sending
    # this connect request is the expected user.
    if request.args.get('state', '') != session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'applicatoin/json'
        return response

    oauth_code = request.args.get('code', '')

    try:
        flow = flow_from_clientsecrets('client_secrets.json', scope='')
        flow.redirect_uri = 'postmessage'
        credentials = flow.step2_exchange(oauth_code)
        cred = pickle.dumps(credentials) # store the credentials for offline access
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'),401)
        response.headers['Content-Type'] = 'application/json'
        return response

    google_username = credentials.id_token['email'].split('@')[0] # google account of the current user
    print "[debug] google user: " + google_username + "@gmail.com has logged in!"
    user = di.find_google_user(google_username)
    if user: # if user has registered in GhostDocs
        user_handle = user.handle
        user.credentials = cred # update credentials
        print "[debug] this google user has already registered as " + user_handle
    else: # if user hasn't registered, create a GhostDocs account. TODO let user choose their username, etc instead of user google username directly.
        user_handle = google_username
        di.create_user(google_username,
                        google_username,
                        user_handle,
                        cred)

    print 'logged in as: ' + user_handle 
    http = httplib2.Http()
    http = credentials.authorize(http)

    # associate the current session with this user
    session['user'] = user_handle

    return redirect('/in/'+user_handle)

# --- API Calls for actions ---
@app.route('/action/open_doc/<doc_id>')
def open_doc(doc_id):
    data = di.user_session.drive.file_by_id(doc_id)
    user = di.db_connector.session().query(di.ghost_db.User).filter(di.ghost_db.User.handle == session["user"]).first()
    return json.dumps({"status": di.add_doc(user, data)})


@app.route('/action/get/settings/<doc_id>/', methods=["GET"])
def get_settings(doc_id):
    doc = di.fetch_doc_by_id(session["user"], doc_id)
    data = {"title": doc.name, "handle": doc.handle}
    return json.dumps(data)


@app.route('/action/post/settings/<doc_id>', methods=["POST"])
def set_settings(doc_id):
    doc = di.fetch_doc_by_id(session["user"], doc_id)
    meta = json.loads(request.data)
    # Need to check the handle to make sure its ok!
    di.update_doc_meta(doc, meta)
    return json.dumps({})


# --- USER PAGE ---

@app.route('/in/<username>')
def render_userpage(username):
    ''' userpage is the page shown to a user after logging in.
        for now, load the newest ghost doc.
    '''
    print '** to find ghostdocs user ' + username + '***'
    user = di.find_ghostdocs_user(username)
    if not user:
        return render_template("404.html")

    docs = di.list_ghost_docs(username)
    if len(docs) == 0:
        # import the first google doc
        doc = di.list_google_docs(username)[0]
        print '...........importing the first google doc into ghostdocs......'
        print doc
        di.add_doc(user, doc)
        docs = di.list_ghost_docs(username)
    else:
        print '...............no need to import...............'
        print len(docs)
        print [x.name for x in docs]

    doc = docs[0]
    dochandle = doc.handle
    return redirect('/in/'+username+'/'+dochandle)
    #return render_base(username, doc['handle'])

# --- EDIT DOC / PREVIEW DOC ---

@app.route('/in/<username>/<dochandle>')
def render_base(username, dochandle):

    # check if the current user has access to this doc
    if not 'user' in session or session['user'] != username:
        return render_template("no_access.html")


    doc = di.load_doc(username, dochandle)
    if not doc:
        return render_template("404.html")
    else:
        di.update_doc_open(doc)
        recent_docs = di.list_recent_docs(doc)
        session["user"] = username
        session["doc"] = dochandle
        return render_template(
            'index.html',
            doc=doc, recent_docs=recent_docs, user=doc.user, CLIENT_ID=CLIENT_ID)


@app.route('/out/<username>/<dochandle>')
def render_publish(username, dochandle):
    doc = di.load_doc(username, dochandle)
    if not doc:
        return render_template("404.html")
    else:
        return render_template('powered.html', doc=doc, user=doc.user)


# --- IFRAME SUPPORT ---


@app.route('/view/<doc_id>')
def render_view(doc_id):
    return di.view_doc(arg_google_doc_id=doc_id)


@app.route('/preview/<doc_id>')
def render_preview(doc_id):
    # should be preview doc, but whatever
    # change this later
    doc = di.load_doc(googledoc_id=doc_id).first()
    return di.preview_doc(userhandle=session['user'], filedict=doc.htmlLink)


@app.route('/publish/<doc_id>')
def publish_doc(doc_id):
    di.publish_doc(userhandle=session['user'], filedict=doc_id)
    status = {}
    status["status"] = "success"
    return json.dumps(status)


# -----------------------

if __name__ == '__main__':
    app.run()
