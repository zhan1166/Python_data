import json
import urllib.error, urllib.parse, urllib.request
import ssl

## Note that Google is increasingly requiring keys
## for this API
##serviceurl = 'http://maps.googleapis.com/maps/api/geocode/json?'
serviceurl = 'http://py4e-data.dr-chuck.net/geojson?'

##Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

while True:
    address = input('Enter location: ')
    if len(address) <1: break

    ##update url and print out the address
    url = serviceurl+urllib.parse.urlencode({'address': address})
    print('Retrieving', url)
    
    ##send the request and read the data
    uh = urllib.request.urlopen(url)
    data = uh.read().decode()
    
    ##print out the length of data
    print('Retrieved',len(data), 'characters')
    ##transfer the data into json format and indents
    js = json.loads(data)
    js_dict = json.dumps(js,indent = 2)
    print(js_dict)
    ##print out the number of remaining approaches
    headers = dict(uh.getheaders())
##    print('Remaining', headers)
    
    ##check if correct status
    if not js or 'status' not in js or js['status'] != 'OK':
        print('================Fail to read data=====================')
        print('js_dict')
        continue
    ##find out the place id and print it
    results = js['results'][0]['place_id']
    print('Place id', results)
    

    
