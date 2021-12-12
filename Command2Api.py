import subprocess
import BaseHTTPServer
import SimpleHTTPServer
import cgi
import threading
import sys
import string
import random

l = []

uri = '/' + ''.join(random.sample(string.ascii_letters+string.digits,8))

class thread(threading.Thread):
	def __init__(self, threadname, command):
		threading.Thread.__init__(self, name='Thread_' + threadname)
		self.threadname = int(threadname)
		self.command = command

	def run(self):
		global l
		ret = subprocess.Popen(
			self.command,
			shell=True,
			stdin=subprocess.PIPE,
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE
		)
		for i in iter(ret.stdout.readline, b""):
			l.append(i.decode().strip())
			print(l)

class ServerHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
	def do_GET(self):
		global l
		if self.path == uri:
			self.wfile.write(l)
			l = []

if __name__ == '__main__':
	# New Thread: Get Command Result
	t1 = thread('1', sys.argv[1])
	t1.start()
	# Webserver
	port = int(sys.argv[2])
	print("URL: http://HOST:{0}{1}".format(port, uri))
	Handler = ServerHandler
	httpd = BaseHTTPServer.HTTPServer(('0.0.0.0', port), Handler)
	httpd.serve_forever()