import cgi
import mail
from http.server import BaseHTTPRequestHandler, HTTPServer

host_name = '127.0.0.1'  # Change this to your Raspberry Pi IP address
host_port = 10001


class MyHandler(BaseHTTPRequestHandler):
    """
    Handles POST requests
    GO to parse_Post
    """

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_HEAD(self, postvars):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def _redirect(self, path):
        self.send_response(303)
        self.send_header('Content-type', 'text/html')
        self.send_header('Location', path)
        self.end_headers()

    def parse_POST(self):
        """Gets post arguments. They should be sent with 'multipart/form-data' header.
        Parses them and sends as bytes to mail.start"""
        ctype, pdict = cgi.parse_header(self.headers['content-type'])
        length = int(self.headers['content-length'])
        postvars = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)
        fr = postvars[b'from']
        subj = postvars[b'subj']
        text = postvars[b'text']
        password = postvars[b'pass']
        spreadsheet = postvars[b'spreadsheet']
        mail.start(fr, subj, text, password, spreadsheet)

    def do_POST(self):
        self.parse_POST()
        # self.do_HEAD(postvars)


if __name__ == '__main__':
    http_server = HTTPServer((host_name, host_port), MyHandler)
    print("Running server on %s:%s" % (host_name, host_port))
    http_server.serve_forever()
