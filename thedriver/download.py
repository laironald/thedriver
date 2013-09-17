import bs4
#import difflib
import os
import re
import time


def download(driv, drive_file, retry=10):
    """Download a file's content.
    Args:
    drive_file: Drive File instance.
      can be dictionary type (more verbose) or just
      plain ol string

    Returns:
    File's content if successful, None otherwise.
    Directly from Google Drive API
    """

    download_url = None
    if type(drive_file).__name__ == "dict":
        if "downloadUrl" in drive_file:
            download_url = drive_file.get('downloadUrl')
        elif "exportLinks" in drive_file:
            download_url = drive_file["exportLinks"]["text/html"]
    elif type(drive_file).__name__ in ('str', 'unicode'):
        download_url = drive_file

    print download_url
    if not download_url:
        return None
    try:
        resp, content = driv.service._http.request(download_url)
    except:
        if retry<=0 :
            print 'Has reached max time of retry... giving up... :('
            return None
        print 'Error while downloading file. About to retry...'
        time.sleep(0.5)
        content = download(driv, drive_file, retry=retry-1)
        return content

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
                    #s.parent.parent.parent.extract()
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

        # 5)
        # Remove extraneous CSS markup
        #bodyclass = soup.body["class"]
        #self.html = re.sub(".%s[{].*?[}]" % bodyclass, "", self.html)

        self.html = self.html.replace(";padding:72pt 72pt 72pt 72pt", "")
