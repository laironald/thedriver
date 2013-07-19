import sys
sys.path.append("..")

import thedriver
import thedriver.download as drived
from flask import Flask, render_template
import hamlish_jinja

#from flask.ext.assets import Environment, Bundle
#from hamlish_jinja import HamlishExtension
#consider Flask-Assets, but sometime later

drive = thedriver.go()
app = Flask(__name__)
app.debug = True

# add haml and compile assets
#https://github.com/Pitmairen/hamlish-jinja
app.jinja_env.add_extension('hamlish_jinja.HamlishExtension')
app.jinja_env.hamlish_enable_div_shortcut = True
#env = Environment(extensions=[HamlishExtension])

#assets = Environment(app)
#assets.url = app.static_url_path
#sass = Bundle('css/base.css.sass', filters='pyscss', output='all.css')
#assets.register('css_all', sass)
#js_bundle = Bundle('js/test.js.coffee', filters='coffeescript', output='all.js')
#assets.register('js_all', js_bundle)

@app.route('/')
def index():
    return render_template('index.html.haml')


@app.route("/ron")
def index2():
    return "FDS"


@app.route('/<title>')
def render_base(title):
    f = drive.files(title=title)
    return render_template('side.html.haml', title=title, embedLink=f[0]["alternateLink"])


@app.route('/right/<title>')
def render_right(title):
    f = drive.files(title=title)
    html = drived.download(drive, f[0])
    out = drived.format(html)
    out.remove_comments()
    return out.html

if __name__ == '__main__':
    app.run()
