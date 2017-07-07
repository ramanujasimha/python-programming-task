import sys
import urllib2
from xml.dom import minidom
import json
import requests

# read command-line argument
try:
	pubmedId = sys.argv[1]
except:
	print "Make sure first argument is a pubmedid"
	sys.exit()

# define urls and parameters for HTTP Get
baseUrlNcbi = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
dbName = "pubmed"
retmodVal = "xml"
fullUrlNcbi = baseUrlNcbi + '?' + 'db=' + dbName + '&' \
		+ 'id=' + pubmedId + '&' + 'retmode=' + retmodVal

# define url HTTP Post
baseUrlReach = "http://agathon.sista.arizona.edu:8080/odinweb/api/text"

def HttpGet(url):
	getResponse = urllib2.urlopen(url)
	xml = minidom.parse(getResponse)

	abstract = ''
	for element in xml.getElementsByTagName('AbstractText'):
		abstract = repr(element.firstChild.nodeValue)

	return abstract

def HttpPost(url, abstract):
	postData = {'text': abstract}
	postResponse = requests.post(url=url, data=postData)

	# save response as json file
	with open(pubmedId+'.json', 'w') as outFile:
		json.dump(postResponse.text, outFile)

	# print statistics
	jsonData = json.loads(postResponse.text)
	print "No. of events:", len(jsonData['events'])
	eventTypes = ''
	for val in jsonData['events']:
		eventTypes += val + ','
	eventTypes = eventTypes.rstrip(',')
	print "Event types:", eventTypes

def main():
	abstract = HttpGet(fullUrlNcbi)
	HttpPost(baseUrlReach, abstract)

if __name__ == "__main__":
	main()

# example test cases
# python ProgrammingTask.py 28546431
# python ProgrammingTask.py 11748933

