from ghost_db import *

connector = GhostDBConnector()
connector.CreateDB()
user = User(**config.get("drive"))

doc = {
    "name": "Testing File",
    "googledoc_id": "1TE0ouM01lsPvot5aZRDv9D7-xC-kLJ0dg3S_zPdWrO4",
    "handle": "testing",
    "html": "".join([x for x in open("ron.html", "rb")])
}
doc = Document(**doc)
user.document.append(doc)
print user.document

connector.session.merge(user)
connector.session.commit()
