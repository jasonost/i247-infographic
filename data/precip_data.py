import requests
from params import token

# set token
head = {'token': token}

# find cities
r = requests.get("http://www.ncdc.noaa.gov/cdo-web/api/v2/locations?datasetid=ANNUAL&locationcategoryid=CITY&limit=1000", headers=head)
results = r.json()['results']
ca_cities = [r for r in results if ', CA US' in r['name']]

# find stations in and around SF
sf = 'CITY:US060031'
r = requests.get("http://www.ncdc.noaa.gov/cdo-web/api/v2/stations?locationid=%s&limit=1000" % sf, headers=head)
results = r.json()['results']

for r in sorted(results, key=lambda x: x['mindate']): print r

# sf station
base_url = "http://www.ncdc.noaa.gov/cdo-web/api/v2/data?datasetid=ANNUAL&datatypeid=TPCP&startdate=1992-01-01&limit=1000"
sta_id = 'COOP:047772'
r = requests.get(base_url + '&stationid=%s' % sta_id, headers=head)
sf_data = r.json()['results']

for s in sf_data: print s['date'][:10], s['value']

# south lake tahoe station
base_url = "http://www.ncdc.noaa.gov/cdo-web/api/v2/data?datasetid=ANNUAL&datatypeid=TSNW&startdate=1992-01-01&limit=1000"
sta_id = 'COOP:048758'
r = requests.get(base_url + '&stationid=%s' % sta_id, headers=head)
tahoe_data = r.json()['results']

for s in tahoe_data: print s['date'][:10], s['value']