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



def look_up(ids: Iterable, auth: str, max_workers: int = 5) -> dict:
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
