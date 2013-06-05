import sys
sys.path.append("..")
import thedriver
import thedriver.download as drived

from flask import Flask, render_template
from flask.ext.assets import Environment, Bundle
from hamlish_jinja import HamlishTagExtension


drive = thedriver.go()
app = Flask(__name__)
app.debug = True

# add haml
app.jinja_env.add_extension(HamlishTagExtension)

# compile assets
assets = Environment(app)
assets.url = app.static_url_path

sass = Bundle('css/base.css.sass', filters='sass', output='all.css')
assets.register('css_all', sass)

#js_bundle = Bundle('js/test.js.coffee', filters='coffeescript', output='all.js')
#assets.register('js_all', js_bundle)


@app.route('/')
def index():
    return render_template('index.html.haml')


@app.route('/<title>')
def render_base(title):
    f = drive.files(title=title)
    print f[0]
    return render_template('side.html.haml', title=title, embedLink=f[0]["alternateLink"])


@app.route('/right/<title>')
def render_right(title):
    f = drive.files(title=title)
    print f
    html = drived.download(drive, f[0])
    out = drived.format(html)
    out.remove_comments()
    return out.html

if __name__ == '__main__':
    app.run()
