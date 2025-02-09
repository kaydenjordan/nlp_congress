import govinfo
import datetime
import scrapelib
import pytz
import cachetools

class GovInfo(scrapelib.Scraper):
    BASE_URL = 'https://www.govinfo.gov/content/pkg/'

    def __init__(self, *args, api_key='DEMO_KEY', **kwargs):
        super().__init__(*args, **kwargs)
        self.headers['X-Api-Key'] = api_key


    def collections(self):
        endpoint = '/collections'
        response = self.get(self.BASE_URL + endpoint)
        return response.json()


    def _format_time(self, dt):

        utc_time = dt.astimezone(pytz.utc)
        time_str = dt.strftime('%Y-%m-%dT%H:%M:%SZ')

        return time_str

    def congressional_hearings(self, start_time=None, end_time=None):
        if start_time is None:
            # the earliest date for this collection
            start_time = datetime.datetime(2018, 6, 5, 0, 0, tzinfo=pytz.utc)
        start_time_str = self._format_time(start_time)

        if end_time is None:
            end_time = datetime.datetime.now(pytz.utc)
        end_time_str = self._format_time(end_time)

        partial = '/collections/CREC/{start_time}'.format(start_time=start_time_str)
        url_template = self.BASE_URL + partial + '/{end_time}'

        seen = cachetools.LRUCache(30)
        for page in self._pages(url_template, end_time_str):
            for package in page['packages']:
                package_id = package['packageId']

                if package_id in seen:
                    continue
                else:
                    # the LRUCache is like a dict, but all we care
                    # about is whether we've seen this package
                    # recently, so we just store None as the value
                    # associated with the package_id key
                    seen[package_id] = None

                response = self.get(package['packageLink'])
                yield response.json()


    def _pages(self, url_template, end_time_str):
        page_size = 100

        params = {'offset':  0,
                  'pageSize': page_size}

        url =  url_template.format(end_time=end_time_str)

        response = self.get(url, params=params)
        data = response.json()

        yield data

        while len(data['packages']) == page_size:

            # the API results are sorted in descending order by timestamp
            # so we can paginate through results by making the end_time
            # filter earlier and earlier
            earliest_timestamp = data['packages'][-1]['lastModified']
            url = url_template.format(end_time=earliest_timestamp)

            response = self.get(url, params=params)
            data = response.json()

            yield data

scraper = govinfo.GovInfo(api_key='gfjuWUAFbyY5u3ELiwYyNsw2pSk537kmtBmctpKN')

# Prints out all the different types of collections available
# in the govinfo API
print(scraper.collections())

# Iterate through every congressional hearing
#
# For congressional hearings you need a specify a start
# date time with a timezone
start_time = datetime.datetime(1990, 1, 1, 0, 0, tzinfo=pytz.utc)


for hearing in scraper.congressional_hearings(start_time):
    link = hearing['download']['pdfLink']
    r = scraper.get(link)
    file = open('testing.txt', 'a')
    file.write(r)
    file.close()