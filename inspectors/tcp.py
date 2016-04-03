from inspector import Inspector
from StringIO import StringIO
import socket

class Tcp(Inspector):
	def __init__(self, driver, ports):
		self._driver = driver

		#Input ports as int, CSV string, or pre-made list
		if isinstance(ports, int):
			self._ports = [ports]
		elif isinstance(ports, str):
			self._ports = map(lambda p: int(p.strip()), ports.split(","))
		elif isinstance(ports, list):
			self._ports = map(lambda p: int(p), ports)
		else:
			raise Exception('Invalid data type for ports')

	def getName(self):
		return "TCP Port %d" % self._port

	def getMetrics(self):
		ret = {}

		for port in self._ports:
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			ret[port] = (sock.connect_ex((self._driver.getHost(), port)) == 0)
			sock.close()

		ret['all'] = len(filter(lambda x: not x, ret.itervalues())) == 0

		return ret

	def getSummary(self):
		metrics = self.getMetrics();

		o = StringIO()
		o.write("## TCP\n")
		for k,v in metrics.iteritems():
			o.write("Port %s: %s\n" % (k, "Open" if v else "Closed"))

		return o.getvalue()


