from ghost_db import *

connector = GhostDBConnector()
connector.CreateDB()
user = User(**config.get("drive"))

doc = {
    "name": "Testing File",
    "googledoc_id": "1TE0ouM01lsPvot5aZRDv9D7-xC-kLJ0dg3S_zPdWrO4",
    "handle": "testing",
    "alternateLink": "https://docs.google.com/feeds/download/documents/export/Export?id=1TE0ouM01lsPvot5aZRDv9D7-xC-kLJ0dg3S_zPdWrO4&exportFormat=html",
    "html": "".join([x for x in open("temp/ron.html", "rb")])
}
doc = Document(**doc)
user.document.append(doc)

connector.session.merge(user)
connector.session.commit()
