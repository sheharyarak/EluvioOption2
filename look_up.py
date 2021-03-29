from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import cpu_count
from typing import Iterable, Tuple
import requests

# Serves as the program that needs to look up information using their item id
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
	return requests.get(
		url= url_prefix + item_id,
		headers = {
			"Authorization" : auth
		}
	)

# serves as the client utility
class ClientUtility:
	"""
	This class serves as the client utility. It's purpose is to
	allow enable multiprocessing while maintaing a limit on the 
	number or simultaneous processes.
	It does the this by using a ProcessPoolExecutor with a max 
	number of workers.
	Since multiprocessing has a hard time pickling lambda 
	functions I have implemented a class that curries a function
	instead.
	"""
	class KeywordCurriedFunction:
		"""
		This class represents a function whose keyword arguments
		have been curried such that only the first argument remains.
		"""
		def __init__(self, fn, **kwargs) -> None:
			"""
			parameters:
			fn:		The function to be curried
			kwargs:	keyword arguments for that fn, except the first

			description:
			stores the function and its argument as part of the object itself.
			"""
			self.fn = fn
			self.kwargs = kwargs
		
		def __call__(self, arg):
			"""
			parameters:
			arg:	the first argument for fn

			description:
			calls fn with arg as the first argument, and the keyword arguments
			stored in self.

			return:
			tuple(arg, result of the function call) 
			"""
			return arg, self.fn(arg, **self.kwargs)

	def __init__(self, fn, max_workers: int = cpu_count(), **kwargs):
		"""
		parameters:
		fn:				the function to be curried.
		max_workers:	the maximum number of processes
		kwargs:			the keyword args for fn, except the first argument

		description: 
		creates a KeywordCurriedFunction and stores it in self. 
		saves the max_workers in self.
		"""
		self.kwcf = ClientUtility.KeywordCurriedFunction(fn, **kwargs)
		self.max_workers = max_workers

	def __call__(self, params: Iterable):
		"""
		parameters:
		params:		an iterable object containing the parameters to be used
					as the first argument for fn
		
		description:
		Uses the ProcessPoolExecutor to allow multiprocessing which enables 
		multiple instances of the program to run simultaneously, for example:
		simultaneous request from an api.
		We iterate through each of the parameters in the Iterable and submit
		the KeywordCurriedFunction with that parameter as its argument to the
		executor.
		As the executor finishes executing we map the results of the program to
		the argument for that result by storing them in a dictionary.

		return:
		dict: arg- > fn(arg) 
		"""
		with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
			results = {}
			futures = []
			for param in params:
				if param not in results.keys():
					results[param] = None
					futures.append(executor.submit(self.kwcf, param))
			for future in as_completed(futures):
				param, result = future.result()
				results[param] = result
			return results



		
		

# def look_up(ids: Iterable, auth: str, max_workers: int = 5, url_prefix='https://eluv.io/items/') -> dict:
# 	"""
# 	args:
# 	ids: an iterable containing Base64 strings referring to item ids
# 	auth: a Base64 string referring to the authentication token
# 	max_workers: maximum number of simultaneous requests

# 	description:
# 	this function iterates through the iterable ids and queues requests 
# 	in the ProcessPoolExecutor. The max_workers limits the number of 
# 	simultaneous requests as required. The results are stored in a
# 	dictionary where the key is the item_id and the value is the response
# 	of the request.

# 	return:
# 	resulting dictionary of id->response pairs.
# 	"""
# 	with ProcessPoolExecutor(max_workers=max_workers) as executor:
# 		results = {}
# 		futures = []
# 		authenticated_req = lambda id: request(id, auth=auth, url_prefix=url_prefix)
# 		for id in ids:
# 			if id not in results.keys():
# 				results[id] = None
# 				futures.append(executor.submit(authenticated_req, id))
# 		for future in as_completed(futures):
# 			id, response = future.result()
# 			results[id] = response
# 		return results
