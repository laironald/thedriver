#from flask.ext.assets import Environment, Bundle
#consider Flask-Assets, but sometime later
#https://github.com/Pitmairen/hamlish-jinja

import sys
#sys.path.append("..")

#import thedriver
#import thedriver.download as drived
from flask import Flask, render_template
from flask import url_for
from flask import send_from_directory
import hamlish_jinja

#drive = thedriver.go()
app = Flask(__name__)
app.debug = True

app.jinja_env.add_extension('hamlish_jinja.HamlishExtension')
app.jinja_env.hamlish_enable_div_shortcut = True


# url_for('static', filename='all.css')


@app.route('/')
def index():
    return render_template('index.html')


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

# @app.route('/<title>')
# def render_base(title):
#     f = drive.files(title=title)
#     return render_template('side.html.haml', title=title, embedLink=f[0]["alternateLink"])

# @app.route('/right/<title>')
# def render_right(title):
#     f = drive.files(title=title)
#     html = drived.download(drive, f[0])
#     out = drived.format(html)
#     out.remove_comments()
#     return out.html

if __name__ == '__main__':
    app.run()
