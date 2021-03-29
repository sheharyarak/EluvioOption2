import requests

ifile = open('random_words.txt', 'r')
ofile = open('ids.txt', 'a')
words = ifile.readlines()
id = 0
url = 'http://127.0.0.1:8000/'
# words = ['sherry', 'dan', 'shaq']
for word in words:
	item = {
		'name': word,
		'description' : 'this is a test word.' 
	}
	x = requests.post(url=url, data=item)
	ofile.write(x.json()['_id'] + '\n')

ofile.close()
ifile.close()