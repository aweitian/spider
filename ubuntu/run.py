# SimpleHTTPServerWithUpload.py
# This code tweaked from https://github.com/tualatrix/tools/blob/master/SimpleHTTPServerWithUpload.py
"""Simple HTTP Server With Upload.
This module builds on BaseHTTPServer by implementing the standard GET
and HEAD requests in a fairly straightforward manner.
"""

__version__ = "1.01"
__all__ = ["SimpleHTTPRequestHandler"]
__author__ = "awei.tian"
__home_page__ = "http://github.com/aweitian"

try:
    import sys
    import os
    import re
    import subprocess
    import BaseHTTPServer
    import json
except ImportError as e:
    # should never be reached
    print ("[f] Required module missing. %s" % e.args[0])
    sys.exit(-1)

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
            cmd = self.rfile.read(int(self.headers['content-length']))
            # r = os.popen(cmd)
            # request = json.loads()
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = p.communicate()
            # print "stdout: '%s'" % stdout
            # print "stderr: '%s'" % stderr
            if stderr != "":
                self.send_response(500)
                self.end_headers()
                self.wfile.write("Error" + stderr)
            else:
                self.send_response(200)
                self.end_headers()
                self.wfile.write(stdout)

            # self.send_header("Welcome", "Contect")

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


if __name__ == '__main__':
    BaseHTTPServer.test(SimpleHTTPRequestHandler, BaseHTTPServer)
