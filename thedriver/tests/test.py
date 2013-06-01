import re
import difflib
import BeautifulSoup

doc = "".join([x for x in open("document.html", "rb")])

close = True
soup = BeautifulSoup.BeautifulSoup(doc)

comments = re.findall("[/][*].*?[*][/]", soup.text)
parentTag = None

for tag in soup.body.findChildren():
    if not comments:
        break
    if parentTag in tag.fetchParents():
        continue
    for i in xrange(1000):  # simulating an infinite loop
        if not comments[0]:
            comments.pop(0)
            if not comments:
                break
        if tag.text == comments[0]:
            comments.pop(0)
            parentTag = tag
            doc = doc.replace(str(tag), "")
            break
        elif tag.text and comments[0].find(tag.text) == 0:
            comments[0] = comments[0][len(tag.text):]
            if i == 0:
                parentTag = tag
            doc = doc.replace(str(tag), "")
            break
        elif tag.text and tag.text.find(comments[0]) == 0:
            sub = comments[0][:len(tag.text)]
            sub = str(tag).replace(sub, "")
            comments[0] = comments[0][len(tag.text):]
            if i == 0:
                parentTag = tag
            doc = doc.replace(str(tag), sub)
            tag = BeautifulSoup.BeautifulSoup(sub)
        else:
            exit = True
            matches = difflib.SequenceMatcher(None, tag.text, comments[0])
            m = matches.get_matching_blocks()[0]
            if m.b == 0 and m.size:
                sub = comments[0][:m.size]
                sub = str(tag).replace(sub, "")
                #this is a bit adhoc. hrm.
                if m.size > 5:
                    sub = re.sub("[/][*].*?[*][/]", "", sub)
                comments[0] = comments[0][m.size:]
                doc = doc.replace(str(tag), sub)
                tag = BeautifulSoup.BeautifulSoup(sub)
                exit = False
            if exit:
                break

open("download.html", "wb").write(doc)
