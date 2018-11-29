#!/Users/ludwig/anaconda3/bin/python
import requests, bs4, sys, re

filename = sys.argv[1]
with open(filename, 'r') as myfile: magmacode = myfile.read()

# Load files
filenames = []
regex = '(?<!\/\/)(?<!\/\/ )load *\"([a-zA-Z0-9_]+\.(?:magma|mg))\";'

def callback(match):
	filename = match.group(1)
	if filename in filenames:
		raise Exception('recursive load')
	with open(match.group(1), 'r') as myfile: return myfile.read()+"\n"

while re.search(regex, magmacode):
	magmacode = re.sub(regex, callback, magmacode)

r = requests.post("http://magma.maths.usyd.edu.au/calc/",
    data={"input": magmacode, "submit": "Submit"},
    headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Safari/605.1.15'}
)
soup = bs4.BeautifulSoup(r.text, features="html.parser")
text = soup.find(id='result').getText()
text = re.sub(' \n   ', '', text)
print (text)
