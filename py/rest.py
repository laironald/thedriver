from flask import Blueprint
from flask import request, session, Blueprint, url_for
import data_interface as di
import json

rest = Blueprint('rest', __name__)

@rest.route('/action/open_doc/<doc_id>')
def open_doc(doc_id):
    user = di.db_connector.session().query(di.ghost_db.User).filter(di.ghost_db.User.handle == session["user"]).first()
    data = di.user_session(session['user']).drive.file_by_id(doc_id)
    url = url_for('render_base',
		username=user.handle, 
	    dochandle=di.add_doc(user, data))
    
    callbackdata = {"status": True, "redirect_url":url}
    return json.dumps(callbackdata)


# settings - make this more restful?

@rest.route('/action/get/settings/<doc_id>/', methods=["GET"])
def get_settings(doc_id):
    doc = di.fetch_doc_by_id(session["user"], doc_id)
    data = {"title": doc.name, "handle": doc.handle}
    return json.dumps(data)

@rest.route('/action/post/settings/<doc_id>', methods=["POST"])
def set_settings(doc_id):
    doc = di.fetch_doc_by_id(session["user"], doc_id)
    meta = json.loads(request.data)
    # Need to check the handle to make sure its ok!
    di.update_doc_meta(doc, meta)
    return json.dumps({})
