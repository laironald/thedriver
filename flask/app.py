#from flask.ext.assets import Environment, Bundle
#consider Flask-Assets, but sometime later
#https://github.com/Pitmairen/hamlish-jinja

import sys
sys.path.append("..")

import data_interface as di
from flask import Flask, render_template
from flask import send_from_directory
import hamlish_jinja
import json

app = Flask(__name__)
app.debug = True

app.jinja_env.add_extension(hamlish_jinja.HamlishExtension)
app.jinja_env.hamlish_enable_div_shortcut = True


# url_for('static', filename='all.css')


@app.route('/')
def index():
    return render_template(
        'index.html',
        title='GhostDocs (>")>',
        googletitle="Testing",
        googledoc="1TE0ouM01lsPvot5aZRDv9D7-xC-kLJ0dg3S_zPdWrO4")


# --- LOGIN / OUT ---


@app.route('/in/<username>/<dochandle>')
def render_base(username, dochandle):
    doc = di.load_doc(username, dochandle)
    if not doc:
        return render_template("404.html")
    else:
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


# --- STATIC FIXTURES ---
# added these to help serve up the static files

@app.route('/css/<path:filename>')
def send_css(filename):
    return send_from_directory('static/css', filename)


@app.route('/js/<path:filename>')
def send_js(filename):
    return send_from_directory('static/js', filename)


@app.route('/img/<path:filename>')
def send_img(filename):
    return send_from_directory('static/img', filename)

# -----------------------

if __name__ == '__main__':
    app.run()
