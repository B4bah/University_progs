from http.server import HTTPServer, CGIHTTPRequestHandler
import os

os.chdir('E:\\Osipov_Michael_20150/pythonProject/University_progs/Server')
server_address = ('', 8000)
httpd = HTTPServer(server_address, CGIHTTPRequestHandler)
httpd.serve_forever()