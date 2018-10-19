# SimpleHTTPServerWithUpload.py
# This code tweaked from https://github.com/tualatrix/tools/blob/master/SimpleHTTPServerWithUpload.py
"""Simple HTTP Server With Upload.
This module builds on BaseHTTPServer by implementing the standard GET
and HEAD requests in a fairly straightforward manner.
"""

__version__ = "0.1"
__all__ = ["SimpleHTTPRequestHandler"]
__author__ = "bones7456"
__home_page__ = "http://li2z.cn/"

import os
import posixpath
import BaseHTTPServer
import urllib
import cgi
import shutil
import mimetypes
import re

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO


class SimpleHTTPRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    server_version = "SimpleHTTPWithUpload/" + __version__

    def do_GET(self):
        # self.protocal_version = 'HTTP/1.1'
        path = self.translate_path(self.path)
        if path == "/":
            self.send_response(200)
            # self.send_header("Welcome", "Contect")
            self.end_headers()
            self.wfile.write(self.path)
        else:
            self.send_response(404)
            # self.send_header("Welcome", "Contect")
            self.end_headers()
            self.wfile.write("Page not found.")
        print "Ok"

    def do_POST(self):
        print "POST"
        path = self.translate_path(self.path)
        if path == "/run":
            self.send_response(200)
            # self.send_header("Welcome", "Contect")
            self.end_headers()
            self.wfile.write(self.rfile.read(int(self.headers['content-length'])))
        else:
            self.send_response(404)
            # self.send_header("Welcome", "Contect")
            self.end_headers()
            self.wfile.write("Page not found.")
        print "Ok"

    def translate_path(self, path):
        """Translate a /-separated PATH to the local filename syntax.
        Components that mean special things to the local file system
        (e.g. drive or directory names) are ignored.  (XXX They should
        probably be diagnosed.)
        """
        # abandon query parameters
        path = path.split('?', 1)[0]
        return path



def test(HandlerClass=SimpleHTTPRequestHandler, ServerClass=BaseHTTPServer.HTTPServer):
    BaseHTTPServer.test(HandlerClass, ServerClass)


if __name__ == '__main__':
    test()
