from concurrent import futures
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import Iterable, Tuple
import requests

def request(item_id: str, auth: str, url_prefix: str) -> Tuple[str, requests.Response]:
	"""
	args:
	item_id: Base64 string referring to the item's id
	auth: Base64 string referring to the authentication token
	url_prefix: url before the item id, example: https://eluv.io/items/

	description:
	this function makes a get request to the url (url_prefix + item_id)
	using the the required headers which in our case is the authentication
	token.

	return:
	item_id, response of the request
	"""
	return item_id, requests.get(
		url= url_prefix + item_id,
		headers = {
			"Authorization" : auth
		}
	)



def look_up(ids: Iterable, auth: str, max_workers: int = 5, url_prefix='https://eluv.io/items/') -> dict:
	"""
	args:
	ids: an iterable containing Base64 strings referring to item ids
	auth: a Base64 string referring to the authentication token
	max_workers: maximum number of simultaneous requests

	description:
	this function iterates through the iterable ids and queues requests 
	in the ProcessPoolExecutor. The max_workers limits the number of 
	simultaneous requests as required. The results are stored in a
	dictionary where the key is the item_id and the value is the response
	of the request.

	return:
	resulting dictionary of id->response pairs.
	"""
	executor = ProcessPoolExecutor(max_workers=max_workers)
	results = {}
	futures = []
	authenticated_req = lambda id: request(id, auth=auth, url_prefix=url_prefix)
	for id in ids:
		if id not in results.keys():
			results[id] = None
			futures.append(executor.submit(authenticated_req, id))
	for future in as_completed(futures):
		id, response = future.result()
		results[id] = response
	return results
