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


# berkeley station
base_url = "http://www.ncdc.noaa.gov/cdo-web/api/v2/data?datasetid=GHCNDMS&datatypeid=TPCP&limit=1000"
berkeley = 'GHCND:USC00040693'
r = requests.get(base_url + '&stationid=%s' % berkeley, headers=head)
results = r.json()['results']

while True:
    cur_max = r.json()['metadata']['resultset']['limit'] + r.json()['metadata']['resultset']['offset'] - 1
    total = r.json()['metadata']['resultset']['count']
    if total < cur_max:
        break
    else:
        r = requests.get(base_url + '&offset=%s&stationid=%s' % (cur_max + 1, berkeley), headers=head)
        results += r.json()['results']


for e in sorted(results, key=lambda x: x['date']):
    print e['date'], e['value']

