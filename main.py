import time
import json
import ssl
from multiprocessing import Pool
import urllib2

def checkAlive(domain):
	try: 
		context = ssl._create_unverified_context()
		return urllib2.urlopen(domain, context=context).getcode()
	except Exception:
		return None

def getHostsAlive(x):
	domain = x['domain']
	return {str(domain):checkAlive(domain)}

def clearTerminal():
	print(chr(27) + "[2J")

def processJson():
	clearTerminal()
	with open('hosts.json') as json_data:
		jsonArray = json.load(json_data)
		pool =  Pool(25)
		statusMap = pool.map(getHostsAlive, jsonArray['hosts'])
		clearTerminal()
		for host in statusMap:
			for domain, code in host.iteritems() :
				if code > 500:
					print '\033[91m'
				elif code >= 400 and code < 500 :
					print '\033[93m'
				elif code == 200:
					print '\033[92m'

				print domain + '\033[0m'

		pool.terminate()

def infiniteLoop():
	while True:
		processJson()
		time.sleep(10)


if __name__ == '__main__':
	infiniteLoop()