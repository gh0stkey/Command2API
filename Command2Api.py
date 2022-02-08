import sys
import uuid
import threading
import subprocess
from http.server import HTTPServer, SimpleHTTPRequestHandler


screen_list = []
uri = '/' + str(uuid.uuid4()).replace("-", "")


class NewThread(threading.Thread):
	def __init__(self, thread_name, command):
		threading.Thread.__init__(self, name='Thread_' + thread_name)
		self.thread_name = int(thread_name)
		self.command = command

	def run(self):
		global screen_list
		ret = subprocess.Popen(
			self.command,
			shell=True,
			stdin=subprocess.PIPE,
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE
		)
		for i in iter(ret.stdout.readline, b""):
			res = i.decode().strip()
			print(res)
			screen_list.append(res)


class ServerHandler(SimpleHTTPRequestHandler):
	def do_GET(self):
		global screen_list
		if self.path == uri:
			self.send_response(200)
			self.send_header('Content-Type', 'text/plain')
			self.end_headers()
			self.wfile.write("\n".join(screen_list).encode())


if __name__ == '__main__':
	# New Thread: Get Command Result
	t1 = NewThread('1', sys.argv[1])
	t1.start()
	# Webserver
	port = int(sys.argv[2])
	print("URL: http://localhost:{0}{1}".format(port, uri))
	httpd = HTTPServer(('0.0.0.0', port), ServerHandler)
	httpd.serve_forever()
