import time
from look_up import *

def test_request():
	id = '6061609d96423061f880b1a5'
	auth = '0'
	url_prefix = 'http://127.0.0.1:8000/'
	res = request(id, auth, url_prefix)
	print('res.text:' + res.text)

def test_client_utility_1000():
	ifile = open('./test_api/ids.txt', 'r')
	ofile = open('out.txt', 'a')
	ids = ifile.read().splitlines()
	# ids = ['6061609d96423061f880b1a5']
	auth = '0'
	url_prefix = 'http://127.0.0.1:8000/'
	cu = ClientUtility(request, max_workers=5, auth=auth, url_prefix=url_prefix)
	results = cu(ids)
	for key in results.keys():
		ofile.write(f'{key} : {results[key].text}\n')

def speed_test_1000():
	"""
	Processor: Intel(R) Core(TM) i5-10210U CPU @ 1.60GHz   2.11 GHz

	8 Workers (API), 5 Workers (Client Utility): --- 13.967503309249878 seconds ---
	8 Workers (API), 1 Workers (Client Utility): --- 77.30586171150208 seconds ---
	8 Workers (API), 8 Workers (Client Utility): --- 11.358855724334717 seconds ---

	Multiproccessing appears to be working on the ClientUtility end.
	
	5 Workers (API), 8 Workers (Client Utility): --- 14.3180513381958 seconds ---
	1 Workers (API), 8 Workers (Client Utility): --- 13.14706540107727 seconds ---
	4 Workers (API), 4 Workers (Client Utility): --- 15.861818313598633 seconds ---

	Multiproccessing appears to be working on the API end.
	"""

	cpus = 8
	print(f'cpus: {cpus}')
	ifile = open('./test_api/ids.txt', 'r')
	ofile = open('out.txt', 'a')
	ids = ifile.read().splitlines()
	# ids = ['6061609d96423061f880b1a5']
	auth = '0'
	url_prefix = 'http://127.0.0.1:8000/'
	cu = ClientUtility(request, max_workers=cpus, auth=auth, url_prefix=url_prefix)
	
	start_time = time.time()
	results = cu(ids)
	end_time = time.time()
	
	for key in results.keys():
		ofile.write(f'{key} : {results[key].text}\n')

	print("--- %s seconds ---" % (end_time - start_time))

def speed_test_500():
	"""
	Processor: Intel(R) Core(TM) i5-10210U CPU @ 1.60GHz   2.11 GHz

	8 Workers (API), 5 Workers (Client Utility): --- 8.200534105300903 seconds ---
	8 Workers (API), 1 Workers (Client Utility): --- 28.965108394622803 seconds ---
	8 Workers (API), 8 Workers (Client Utility): --- 6.49934983253479 seconds ---

	Multiproccessing appears to be working on the ClientUtility end.
	
	5 Workers (API), 8 Workers (Client Utility): --- 11.06765866279602 seconds ---
	1 Workers (API), 8 Workers (Client Utility): --- 8.73393201828003 seconds ---
	4 Workers (API), 4 Workers (Client Utility): --- 10.785058736801147 seconds ---

	Multiproccessing appears to be working on the API end.
	"""

	cpus = 4
	print(f'cpus: {cpus}')
	ifile = open('./test_api/ids.txt', 'r')
	ofile = open('out.txt', 'a')
	ids = ifile.read().splitlines()[:500]
	# ids = ['6061609d96423061f880b1a5']
	auth = '0'
	url_prefix = 'http://127.0.0.1:8000/'
	cu = ClientUtility(request, max_workers=cpus, auth=auth, url_prefix=url_prefix)
	
	start_time = time.time()
	results = cu(ids)
	end_time = time.time()
	
	for key in results.keys():
		ofile.write(f'{key} : {results[key].text}\n')

	print("--- %s seconds ---" % (end_time - start_time))






if __name__ == '__main__':   
	# test_request() 
	# test_client_utility_1000()
	speed_test_1000()