import bs4
#import difflib
import os
import re


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

    def text_plus(self, soup):
        """
        Extract extra content about the text (like Images)
        """
        if type(soup).__name__ == "str":
            soup = bs4.BeautifulSoup(soup)
        imgs = ["[img: {}]".format(x.get("src")) for x in soup.find_all("img")]
        return soup.get_text() + "".join(imgs)

    def remove_comments(self):
        if not self.parse:
            self.set_parse()

        # a)
        # remove google doc-esque comments
        # remove google doc-esque footnotes (do we want to delete?)
        soup = bs4.BeautifulSoup(self.html)
        for s in soup.findAll("a"):
            if s.get("href") and "#cmnt" in s.get("href"):
                if "cmnt_" in s.get("name"):
                    s.parent.extract()
                elif "#cmnt_" in s.get("href"):
                    s.parent.parent.extract()
            elif s.get("href") and "#ftnt" in s.get("href"):
                if "ftnt_" in s.get("name"):
                    s.parent.extract()
                elif "#ftnt_" in s.get("href"):
                    s.parent.parent.parent.extract()
                    s.parent.parent.extract()
        self.html = soup.encode("ascii")

        # 1)
        # remove exact text matches
        soup = bs4.BeautifulSoup(self.html)
        comments = re.findall(self.parse, self.html)
        commentt = [self.text_plus(k) for k in comments]
        parentTag = None
        for tag in soup.body.findChildren():
            if not comments:
                break
            if parentTag in tag.fetchParents():
                continue
            if self.text_plus(tag) in commentt:
                idx = commentt.index(tag.get_text())
                # print comments[idx]
                comments.pop(idx)
                commentt.pop(idx)
                parentTag = tag
                tag.extract()
                # print tag
                # print "------"
        self.html = soup.encode("ascii")

        #NOTE THIS STRIPS TOO MUCH CONTENT. TWO IMAGES? WTF!

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
                self.html = self.html.replace(re.findall(self.parse, str(tag))[0], "")

        # 4)
        # catch-all. note, we probably want to change this as
        # it might be too aggressive
        comments = re.findall(self.parse, self.html)
        for c in comments:
            self.html = self.html.replace(c, "")

        # 5) TODO?
        """
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

            m = difflib.SequenceMatcher(None, str(tag), comments[0])
            m = m.get_matching_blocks()[0]
            n = difflib.SequenceMatcher(None, tag.text, commentt[0])
            n = n.get_matching_blocks()[0]

            if m.b == 0 and m.size:
                print "==="
                print comments[0]
                print len(comments[0]), len(commentt[0])
                # decision elimate everything OR keep tag?
                if n.a == 0 and n.size == len(tag.text):
                    tag.extract()
                elif tag.string:
                    tag.string.replace_with(tag.text[:n.a] + tag.text[n.a+n.size:])
                else:
                    newt = soup.new_tag("a")
                    newt.string = "LiWeN"
                    tag.replace_with(newt)

                parentTag = tag
                comments[0] = comments[0][m.size:]
                commentt[0] = commentt[0][n.size:]

                print len(comments[0]), len(commentt[0])
                print tag

            if not (comments[0] and commentt[0]):
                comments.pop(0)
                commentt.pop(0)
        self.html = soup.encode("ascii")
        """
        pass
