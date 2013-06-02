import os
import re
import difflib
import bs4


def download(driv, drive_file):
    """Download a file's content.
    Args:
    drive_file: Drive File instance.

    Returns:
    File's content if successful, None otherwise.
    Directly from Google Drive API
    """
    if "downloadUrl" in drive_file:
        download_url = drive_file.get('downloadUrl')
    elif "exportLinks" in drive_file:
        download_url = drive_file["exportLinks"]["text/html"]
    else:
        download_url = None
    if not download_url:
        return None
    resp, content = driv.service._http.request(download_url)
    if resp.status == 200:
        return content
    else:
        print 'An error occurred: %s' % resp
        return None


class format():
    parse = None

    def __init__(self, html):
        if os.path.exists(html):
            html = "".join([x for x in open(html, "rb")])
        self.html = html

    def set_parse(self, parse="/**/"):
        p_len = len(parse)/2
        p_x = parse[:p_len]
        p_y = parse[p_len:]
        self.parse = "[{}].*?[{}]".format("][".join(p_x), "][".join(p_y))

    def remove_comments(self):
        if not self.parse:
            self.set_parse()

        # 0)
        # remove google doc-esque comments
        soup = bs4.BeautifulSoup(self.html)
        for s in soup.findAll("a"):
            if s.get("href") and "#cmnt" in s.get("href"):
                if "cmnt_" in s.get("name"):
                    self.html = self.html.replace(unicode(s.parent), "")
                elif "#cmnt_" in s.get("href"):
                    self.html = self.html.replace(unicode(s.parent.parent), "")

        soup = bs4.BeautifulSoup(self.html)
        comments = re.findall(self.parse, soup.text)
        parentTag = None

        # 1)
        # remove exact text matches
        for tag in soup.body.findChildren():
            if not comments:
                break
            if parentTag in tag.fetchParents():
                continue
            if tag.text in comments:
                idx = comments.index(tag.text)
                comments.pop(idx)
                parentTag = tag
                tag.extract()
        self.html = unicode(soup)

        # 2)
        # search for blocks of comments that lead with /* and end with */
        # removes the closest tags
        comments = re.findall(self.parse, self.html)
        for c in comments:
            idx = self.html.index(c)
            if self.html[idx-1] == ">" and self.html[idx+len(c)] == "<":
                rdx = self.html.rfind("<", 0, idx)
                ldx = self.html.find(">", idx+len(c)) + 1
                self.html = self.html.replace(self.html[rdx:ldx], "")

        # 3)
        # delete inline comments /* */ in one line
        parentTag = None
        soup = bs4.BeautifulSoup(self.html)
        for tag in soup.body.findChildren():
            if parentTag in tag.fetchParents():
                continue
            if re.findall(self.parse, tag.text):
                parentTag = tag
                self.html = self.html.replace(re.findall(self.parse, unicode(tag))[0], "")

        # 4)
        reach = False
        parentTag = None
        soup = bs4.BeautifulSoup(self.html)
        comments = re.findall(self.parse, self.html)
        commentt = re.findall(self.parse, soup.text)
        for c in comments:
            print c
        print ""
        for tag in soup.body.findChildren():
            if parentTag in tag.fetchParents():
                continue

            m = difflib.SequenceMatcher(None, unicode(tag), comments[0])
            m = m.get_matching_blocks()[0]
            n = difflib.SequenceMatcher(None, tag.text, commentt[0])
            n = n.get_matching_blocks()[0]

            if m.b == 0 and m.size:
                reach = True
                print "==="
                print comments[0]
                # decision elimate everything OR keep tag?
                if n.a == 0 and n.size == len(tag.text):
                    killTag = True
                    tag.extract()
                else:
                    killTag = False
                    print [x for x in tag.findChildren()]
                    tag.replaceWith(soup.newTag("RON<br/>"))

                parentTag = tag
                comments[0] = comments[0][m.size:]
                commentt[0] = commentt[0][n.size:]

                print comments[0]
                print tag
                print killTag

            if reach:
                print "--------"
                print m.b, m.size, n.b, n.size
                print tag.text
                print commentt[0]
                print tag

            if not (comments[0] and commentt[0]):
                comments.pop(0)
                commentt.pop(0)
        self.html = unicode(soup)

r = format("tests/document.html")
r.remove_comments()
open("tests/download.html", "wb").write(r.html)
print r.html
