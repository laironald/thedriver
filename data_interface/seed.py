from ghost_db import *

connector = GhostDBConnector()
connector.CreateDB()
user = User(**config.get("drive"))

docs = [{
    "name": "Testing File",
    "googledoc_id": "1TE0ouM01lsPvot5aZRDv9D7-xC-kLJ0dg3S_zPdWrO4",
    "handle": "testing",
    "htmlLink": "https://docs.google.com/feeds/download/documents/export/Export?id=1TE0ouM01lsPvot5aZRDv9D7-xC-kLJ0dg3S_zPdWrO4&exportFormat=html",
    "alternateLink": "https://docs.google.com/document/d/1TE0ouM01lsPvot5aZRDv9D7-xC-kLJ0dg3S_zPdWrO4/edit?usp=drivesdk",
    "html": "".join([x for x in open("temp/ron.html", "rb")])
}, {
    "googledoc_id": "1fujSnqrwXBOHvrTgOd-pnOdY8BhmMhxKJObujpaMFvc",
    "name": "Testing2",
    "htmlLink": "https://docs.google.com/feeds/download/documents/export/Export?id=1fujSnqrwXBOHvrTgOd-pnOdY8BhmMhxKJObujpaMFvc&exportFormat=html",
    "alternateLink": "https://docs.google.com/document/d/1fujSnqrwXBOHvrTgOd-pnOdY8BhmMhxKJObujpaMFvc/edit?usp=drivesdk",
    "handle": "testing2",
    "html": "".join([x for x in open("temp/ron.html", "rb")])
}, {
    "googledoc_id": "1uWrCtM9xJ7mu1acCeAENZdlQY9rjRMnY7YBYuxJZPKA",
    "name": "Testing3",
    "htmlLink": "https://docs.google.com/feeds/download/documents/export/Export?id=1uWrCtM9xJ7mu1acCeAENZdlQY9rjRMnY7YBYuxJZPKA&exportFormat=html",
    "alternateLink": "https://docs.google.com/document/d/1uWrCtM9xJ7mu1acCeAENZdlQY9rjRMnY7YBYuxJZPKA/edit?usp=drivesdk",
    "handle": "testing3",
    "html": "".join([x for x in open("temp/ron.html", "rb")])
}]

for doc in docs:
    doc = Document(**doc)
    user.document.append(doc)

connector.session().merge(user)
connector.session().commit()
