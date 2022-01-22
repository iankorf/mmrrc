import argparse
import json
import sys
import time
import urllib
import urllib.request

parser = argparse.ArgumentParser(description='Publications printer')
parser.add_argument('--pmcid', required=False, type=str,
	nargs='+', metavar='<PMCID>', help='PubMed Central ID')
parser.add_argument('--file', required=False, type=str,
	metavar='<FILE>', help='file of PMCIDs')
arg = parser.parse_args()

pmcids = []
if arg.pmcid:
	for pmcid in arg.pmcid:
		pmcids.append(pmcid)
if arg.file:
	with open(arg.file) as fp:
		for line in fp.readlines():
			line = line.rstrip()
			pmcids.append(line)

URL = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pmc&retmode=json&id='

for pmcid in pmcids:
	j = json.loads(urllib.request.urlopen(f'{URL}{pmcid}').read())
	print(json.dumps(j, indent=4))
	journal = j['result'][f'{pmcid}']['source']
	author = j['result'][f'{pmcid}']['authors'][0]['name']
	title = j['result'][f'{pmcid}']['title']
	pmid = None
	for thing in j['result'][f'{pmcid}']['articleids']:
		if thing['idtype'] == 'pmid': pmid = thing['value']
	if pmid == None:
		print('error in getting pmid')
		sys.exit(1)
	link = f'https://pubmed.ncbi.nlm.nih.gov/pmid'
	
	print(journal, author, link, title)
	time.sleep(0.1) # don't spam them


"""

create html, open in safari, paste into google doc

"""