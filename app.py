#from flask.ext.assets import Environment, Bundle
#consider Flask-Assets, but sometime later
#https://github.com/Pitmairen/hamlish-jinja

import data_interface as di
import hamlish_jinja
import json
from flask import Flask, render_template

app = Flask(__name__, static_folder='static', static_url_path='')
app.debug = True

app.jinja_env.add_extension(hamlish_jinja.HamlishExtension)
app.jinja_env.hamlish_enable_div_shortcut = True


# url_for('static', filename='all.css')


@app.route('/')
def index():
    return render_template('welcome.html')


# --- EDIT DOC / PREVIEW DOC ---


@app.route('/in/<username>/<dochandle>')
def render_base(username, dochandle):
    doc = di.load_doc(username, dochandle)
    if not doc:
        return render_template("404.html")
    else:
        di.update_doc_open(doc)
        di.list_recent_docs(doc)
        return render_template('index.html', doc=doc, user=doc.user)


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
    return di.preview_doc(filedict=doc.htmlLink)


@app.route('/publish/<doc_id>')
def publish_doc(doc_id):
    di.publish_doc(filedict=doc_id)
    status = {}
    status["status"] = "success"
    return json.dumps(status)


# -----------------------

if __name__ == '__main__':
    app.run()
