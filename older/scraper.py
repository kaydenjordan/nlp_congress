#For getting congressional data
#Open scraper.py and change file name on line 66
#Run scraper.py dd/mm/yyyy - dd/mm/yyyy
#Open getcongress2.py and change filenames on lines 17,23,92,109,120
#Run getcongress2.py
#!/usr/bin/python

import urllib,  os, datetime, re, sys,  zipfile
import zipfile, requests
import time
import io as BytesIO
try:
    import json
except:
    import simplejson as json


class CRScraper(object):
    def __init__(self):
        # use httplib so that we can retrieve the headers before retrieving the
        # body.
        self.domain = "www.gpo.gov"
        self.path = "/fdsys/pkg/"
        self.date = None
        self.datestring = None
        self.url = None
        self.zipsize = None

    def set_date(self, date):
        ''' given a date object, retrieve the documents for that given date and
        save them to the filesystem.'''
        self.date = date
        self.datestring = date.strftime("%Y-%m-%d")
        self.url = self.path + "CREC-%s.zip" % self.datestring

    def was_in_session(self):
        # # check the response header to make sure the Record exists for this date.
        # conn = httplib.HTTPConnection(self.domain, timeout=25)
        # conn.request("HEAD", self.url)
        # # the connection can be a little dodgy, let it try connecting a few
        # # times if needed.
        # could_not_connect = 0
        # while could_not_connect < 3:
            # try:
                # resp = conn.getresponse()
                # could_not_connect = False
                # break
            # except:
                # could_not_connect += 1
        # if could_not_connect:
            # return None

        # content_type = resp.getheader('content-type')
        # if content_type != 'application/zip':
            # print 'Congress was not in session on %s' % self.datestring
            # return False
        # self.zipsize = resp.getheader('content-length')
        return True

    def retrieve(self):
	    proxy = {'https': 'http://65.36.123.172', 'http': 'http://65.36.123.172'}
	    zip = requests.get('http://' + self.domain + self.url, stream=True, proxies = proxy)
	    print(zip)
	    z = zipfile.ZipFile(BytesIO.BytesIO(zip.content))
	    names = z.namelist()
	    f = "D:/Dropbox/"+"2017 urls_2.txt"
	#print names
	    tmp = open(f, "ab")
	#tmp.write(names)
	#tmp.close()
	    print('retrieving zip file %s. this could take a few mins...' % tmp)		
	#rawdata = strzip.read()
	#urls = re.findall("(CREC.+?\.htm)", rawdata)
	    for name in names:
		    tmp.write(name)
	    tmp.close()
	#else: print '%s exists. skipping download' % tmp

	# prepare the directory to copy the zipped files into. use strftime
	# here to ensure day and month directories are always 2 digits.
	    save_path = os.path.join(CWOD_HOME, 'raw/%d/%s/%s/' % (self.date.year, self.date.strftime("%m"), self.date.strftime("%d")))
	    if not os.path.exists(save_path):
		    os.makedirs(save_path)

	    return save_path

    def log_download_status(self, datestring, status):
        if not os.path.exists(SCRAPER_LOG):
            if not os.path.exists(LOG_DIR):
                os.makedirs(LOG_DIR)
            scraper_log = open(SCRAPER_LOG, 'w')
            scraper_log.write('Date, Status\n')
            scraper_log.close()

        scraper_log = open(SCRAPER_LOG, 'r')
        scraper_lines = scraper_log.readlines()
        scraper_log.close()
        update_line = None
        # if this date is already in the log file, update it.
        for linenum, logline in enumerate(scraper_lines):
            if datestring in logline:
                # update the status of that line
                update_line = linenum
        if update_line:
            scraper_lines[update_line] = '%s, %s\n' % (datestring, status)
        # if the date was not already in the log file, append it at the end
        else:
            scraper_lines.append('%s, %s\n' % (datestring, status))
        scraper_log = open(SCRAPER_LOG, 'w')
        scraper_log.writelines(scraper_lines)
        scraper_log.close()

    def previously_retrieved(self):
        # datestring = self.date.strftime("%d/%m/%Y")
        # if not os.path.exists(SCRAPER_LOG):
             # return False
        # scraper_lines = open(SCRAPER_LOG).readlines()
        # for line in scraper_lines:
            # if datestring in line and 'success' in line:
                # print 'This date was previously retrieved: Record already exists\n'
                # return True
            # if datestring in line and 'nosession' in line:
                # print 'This date was previously retrieved: Congress was not in session.\n'
                # return True
        return False

    def retrieve_by_date(self, date):
        self.set_date(date)
        if not self.previously_retrieved():
            in_session = self.was_in_session()
            if in_session:
                path = self.retrieve()
                return path
            elif in_session == False:
                datestring = self.date.strftime("%d/%m/%Y")
                self.log_download_status(datestring, 'nosession')
            elif in_session == None:
                self.log_download_status(self.date.strftime("%d/%m/%Y"), 'GPO connection error')

def date_from_string(datestring):
    return datetime.datetime.strptime(datestring, "%d/%m/%Y")

def daterange_list(start, end):
    ''' returns a list of date objects between a start and end date. start must
    come before end. '''
    daterange = (end - start).days
    dates = [start + datetime.timedelta(n) for n in range(daterange)]
    return dates

def usage():
    return '''
Several ways to invoke the scraper:
0. "./scraper.py" will display this message (and do nothing)
1. "./scraper.py all" will go back in time retrieving all daily congressional records until the date specified as OLDEST_DATE in settings.py. You probably want to use this with caution, but it can be useful during initial setup.
2. "./scraper.py backto dd/mm/yyyy" will retrieve congressional records back to the date given.
3. "./scraper.py dd/mm/yyyy - dd/mm/yyyy" will retreive congressional records for all days within the range given. the first date should occur before the second date in time.
4. "./scraper.py dd/mm/yyyy" will retreive the congressional record for the day given.
    '''

def run_scraper(date):
    ''' Returns True if there were records to retrieve, and False is congress
    was not in session '''
    return CRScraper().retrieve_by_date(date)



if __name__ == '__main__':

    if len(sys.argv) == 1:
        print(usage())
        sys.exit()
    try:
        if len(sys.argv) == 2:
            if sys.argv[1] == 'all':
                end = datetime.datetime.now()
                start = date_from_string(OLDEST_DATE)
                dates = daterange_list(start, end)
            else:
                dates = [date_from_string(sys.argv[1])]

        elif len(sys.argv) == 3 and sys.argv[1] == 'backto':
            end = datetime.datetime.now()
            start = date_from_string(sys.argv[2])
            dates = daterange_list(start, end)

        elif len(sys.argv) == 4:
            start = date_from_string(sys.argv[1])
            end = date_from_string(sys.argv[3])
            dates = daterange_list(start, end)

        else:
            raise Exception

    except:
        print(usage())
        print('There was an error: ')
        sys.exit()

    for date in dates:
        print("Checking Congressional Record for %s" % date)
        if CRScraper().retrieve_by_date(date):
            print('Will now sleep for 10 seconds before retrieving next record...zzz...')
            time.sleep(10)
        else:
            if len(dates) == 1:
                sys.exit()
            else:
                #print 'sleeping for 5 seconds...zzz...'
                #time.sleep(5)
                continue