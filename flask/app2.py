import sys
sys.path.append("..")

import thedriver
import thedriver.download as drived
from flask import Flask, render_template
from flask.ext.assets import Environment, Bundle
from hamlish_jinja import HamlishExtension

drive = thedriver.go()
app = Flask(__name__)
app.debug = True


@app.route('/')
def index():
    return "Hello"


@app.route("/ron")
def index2():
    return "FDS"


@app.route('/<title>')
def render_base(title):
    return title


if __name__ == '__main__':
    app.run()
