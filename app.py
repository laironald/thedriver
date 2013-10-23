#from flask.ext.assets import Environment, Bundle
#consider Flask-Assets, but sometime later
#https://github.com/Pitmairen/hamlish-jinja

#flask blueprints
#http://flask.pocoo.org/docs/blueprints/

#import hamlish_jinja
import json
import random
import string
import os

path=os.path.dirname(os.path.realpath(__file__))
os.chdir(path) # change working directory to folder of this app.py

from flask import Flask, render_template
from flask import request, session, url_for

import data_interface as di

# Blueprints
from py.auth import auth
from py.rest import rest


app = Flask(__name__, static_folder='static', static_url_path='')
app.register_blueprint(auth)
app.register_blueprint(rest)
app.debug = di.config.get("global").get("app_debug")

#app.jinja_env.add_extension(hamlish_jinja.HamlishExtension)
#app.jinja_env.hamlish_enable_div_shortcut = True
app.secret_key = di.config.get("global").get("secret")

CLIENT_ID = json.loads(open('client_secrets.json','r').read())['web']['client_id']
# url_for('static', filename='all.css')


# ------- error handling ----------

@app.errorhandler(404)
@app.errorhandler(500)
def page_not_found(e):
    if app.debug:
        return e
    else:
        return render_template("page_not_found.html")

@app.route('/')
def welcome():
    '''Initialize a session for the current user, and render welcome.html.'''
    '''Show log-in botton if user hasn't logged in.'''
    # Create a state token.
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    session['state'] = state
    return render_template('views/welcome.html', STATE = state, CLIENT_ID=CLIENT_ID)

# --- USER PAGE ---

@app.route('/in/<username>')
def profile(username):
    ''' userpage is the page shown to a user after logging in.
        for now, load the newest ghost doc.
    '''
    print '** to find ghostdocs user ' + username + '***'
    user = di.find_ghostdocs_user(username)
    recent_docs = di.list_recent_docs(user=user)
    return render_template("views/profile.html", 
        recent_docs=recent_docs, user=user)

# --- EDIT DOC / PREVIEW DOC ---

@app.route('/in/<username>/<dochandle>')
def editor(username, dochandle):

    # check if the current user has access to this doc
    if (not 'user' in session or session['user']!=username) and username!='ghostie':
        return render_template("views/page_not_found.html")

    doc = di.load_doc(username, dochandle)
    di.update_doc_open(doc)
    recent_docs = di.list_recent_docs(doc)
    session["user"] = username
    session["doc"] = dochandle
    return render_template(
        'views/editor.html',
        doc=doc, recent_docs=recent_docs, user=doc.user, CLIENT_ID=CLIENT_ID)


@app.route('/out/<username>/<dochandle>')
def document(username, dochandle):
    doc = di.load_doc(username, dochandle)
    return render_template('views/document.html', doc=doc, user=doc.user)


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
