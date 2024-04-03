from urllib.request import Request, urlopen
import requests
import urllib.request
from requests.auth import HTTPBasicAuth

#https://www.govinfo.gov/content/pkg/CREC-2020-07-27/pdf/CREC-2020-07-27-senate.pdf
dates = ["2020-07-27", "2020-07-26","2020-07-25","2020-07-24"]
chamber = 'senate'
for date in dates:
    url = 'https://www.govinfo.gov/content/pkg/CREC-' + date + '/pdf/CREC-' + date + '-' + chamber + '.pdf'
    auth = HTTPBasicAuth('apikey', 'fRzOFJAn2gaPkMKgqaVlgVeZvmxR0l1yufNjzueT')
    #req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'}, auth=auth)
    r = requests.get(url, auth=auth)
    print(r.content)
    outfile = chamber + '_' + date + '.pdf'
    with open(outfile, "wb") as code:
        code.write(r.content)