import os


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
    import re
    import difflib
    import BeautifulSoup

    def __init__(self, html):
        if os.path.exists(html):
            html = "".join([x for x in open(html, "rb")])
        self.html = html
