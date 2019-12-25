import urllib.request, urllib.parse, urllib.error
import json
import sqlite3
import csv
from itertools import islice
import time
import socket

#Read csv file
filename = 'sg.csv'
handle = csv.reader(open(filename,'r'))
#Set default time for the program, if the url.request.read() could not respond in this time interval
#Then resend the url request to the API
socket.setdefaulttimeout(60)


#Create new table
connection = sqlite3.connect('map_market.sqlite')
cur = connection.cursor()
##cur.executescript('''
##DROP TABLE IF EXISTS City;
##DROP TABLE IF EXISTS Area;
##DROP TABLE IF EXISTS Map;
##DROP TABLE IF EXISTS Code;
##DROP TABLE IF EXISTS Region;
##
##CREATE TABLE Region(
##    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
##    name TEXT,
##    address TEXT,
##    area TEXT,
##    latitude TEXT,
##    longitude TEXT,
##    telephone TEXT
##);
##
##CREATE TABLE City(
##    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
##    city_code TEXT UNIQUE
##);
##
##CREATE TABLE Area(
##    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
##    city_id INTERGER UNIQUE,
##    area TEXT UNIQUE
##);
##
##CREATE TABLE Code(
##    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
##    code TEXT UNIQUE
##);
##
##CREATE TABLE Map(
##    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
##    code_id INTEGER,
##    name TEXT,
##    address TEXT,
##    area_id INTEGER,
##    latitude TEXT,
##    longitude TEXT,
##    telephone TEXT
##)''')

##Drop the table at begining


##cur.executescript('''
cur.executescript('''
DROP TABLE IF EXISTS Map;
DROP TABLE IF EXISTS Region;
                  
CREATE TABLE Region(
    id INTEGER,
    name TEXT,
    address TEXT,
    area  TEXT,
    latitude  TEXT,
    longitude  TEXT,
    telephone  TEXT
);

CREATE TABLE Map(
    city TEXT,
    area TEXT,
    code TEXT,
    name TEXT,
    address TEXT,
    latitude  TEXT,
    longitude  TEXT,
    telephone  TEXT
)''')




output = '&output=json'
##ak = '&ak=ObO2u9Omrm03o6PnlGNMx3RdGis4kFCc&sn=e87f244acc615e2aa88d7b8f46760087'
ak = '&ak=aqf0Ujiv1dEmESzSSBZv5FwjciY9uZ3L'

#parameter
n = 0

## Define a function to read the jason data
def data_reading(url):
    uh = urllib.request.urlopen(url,timeout=60)
##print out the headers
##    headers = dict(uh.getheaders())
##    print(headers)
    data = uh.read().decode()
    print('Retrieved', len(data), 'characters')
    try:
        js = json.loads(data)
    except:
        js = None
    return js, data


## Define Search class
class SEARCH(object):
    
    def __init__(self):
        print('Initializing')
    ##region search
    def region(self,address):
        key = 0
        print('Region Searching...........')
        for p in range(5):
            url = urllib.request.quote(port+'?'+query+address+pages+str(p)+output+ak,'/:=&?#+!$,;@()*[]')
            [js,data] = data_reading(url)
            #error message
            if 'status' not in js or js['status']!=0:
                print('===============Fail To Retrieve ================')
                print(data)
                continue
            while True:
                try:
                    name = js['results'][n]['name']
                    ad = js['results'][n]['address']
                    area = js['results'][n]['area']
                    lat = js['results'][n]['location']['lat']
                    lng = js['results'][n]['location']['lng']
                    try: 
                        phone = js['results'][n]['telephone']
                    except:
                        phone = ''
                    key+=1
                    cur.execute("INSERT OR IGNORE INTO Region VALUES(?,?,?,?,?,?,?)",(key,name,ad,area,lat,lng,phone))
                    n = n+1
                except:
                    break
            n = 0
            connection.commit()
        cur.close()
        connection.close()
    ##Coordinates search
    def coord(self):
        print('Coordinates Searching...........')
        [js,data] = data_reading(url)
        try:
            level = js['result']['level']
            precision = js['result']['precise']
            confidence = js['result']['confidence']
            lat = js['result']['location']['lat']
            lng = js['result']['location']['lng']
##            print('Type of the address', level)
##            print('Precision', precision)
##            print('Confidence level', confidence)
##            print('Location latitude', lat)
##            print('Location longitude', lng)
        except:
            print('Error!!!')
    ##Square area search
    def area(self):
        key = 0
        print('Area Searching............')

        for line in islice(handle,1,None):
            code = str(line[1])
##            ## The program breaks, and restart it at specified line
##            if (key == 0)&(code !='WZ1202'): continue
##            key = 1
            
            LL_lat = line[2] #left_lower latitude
            LL_long = line[4] #lef_lower longitude
            RU_lat = line[3] #Right_upper latitude
            RU_long = line[5] #Right_upper longitude
            for p in range(3):
                url = urllib.request.quote(port+'?'+query+bounds+str(LL_lat)+','+str(LL_long)+','\
                                       +str(RU_lat)+','+str(RU_long)+pages+str(p)+output+ak,'/:=&?#+!$,;@()*[]')
                try:
                    [js,data] = data_reading(url)
                    if js["total"] == 0: break
                except:
                    break
                #error message
                if 'status' not in js or js['status']!=0:
                    print('===================Fail To Retrieve ======================')
                    print(data)
                    continue
                while True:
                    try:
                        city = js['results'][n]['city']
                        name = js['results'][n]['name']
                        ad = js['results'][n]['address']
                        area = js['results'][n]['area']
                        lat = (js['results'][n]['location']['lat'])
                        lng = (js['results'][n]['location']['lng'])
                        try:
                            phone = (js['results'][n]['telephone'])
                        except:
                            phone = ''
                        cur.execute('''INSERT OR IGNORE INTO Map VALUES(?,?,?,?,?,?,?,?)''',\
                                    (city, area, code, name, ad, lat, lng, phone))
                        
##                        cur.execute('''INSERT OR IGNORE INTO City (city_code) VALUES(?)''',(city,))
##                        cur.execute('SELECT id FROM City WHERE city_code = ?',(city,))
##                        city_id = cur.fetchone()[0]
##                        print(city_id)
##                        cur.execute('''INSERT OR IGNORE INTO Area (city_id, area) VALUES(?,?)''', (city_id,area))
##                        cur.execute('SELECT id FROM Area WHERE area = ?', (area,))
##                        area_id = cur.fetchone()[0]
##
##                        cur.execute('''INSERT OR IGNORE INTO Code (code) VALUES(?)''', (code,))
##                        cur.execute('SELECT id FROM Code WHERE code = ?', (code,))
##                        code_id = cur.fetchone()[0]
##
##                        key+=1
##                        cur.execute('''INSERT OR REPLACE INTO Map
##                            VALUES(?,?,?,?,?,?,?)''', (code_id, name, ad, area_id, lat, lng, phone))
                        connection.commit()
                        n = n+1
                    except:
                        break
                n = 0
        cur.close()
        connection.close()

                
while True:
    ask = input('Enter searching object\n0——地点周围目标搜索\n1——\
    目标地经纬度搜索\n2——矩形区域搜索\n')
    if ask =='0':
        address = input('Enter region: ')
        if len(address) < 1: break
        port = 'http://api.map.baidu.com/place/v2/search'
        query = 'query=ATM机&tag=银行&region='
        pages = '&page_size=20&page_num='
        attemp = SEARCH()
        attemp.region(address)

    elif ask =='1':
        address = input('Enter region: ')
        if len(address) < 1: break
        port = 'http://api.map.baidu.com/geocoder/v2/'
        query = 'address='
        url = urllib.request.quote(port+'?'+query+address+output+ak+sn,'/:=&?#+!$,;@()*[]')
        attemp = SEARCH()
        attemp.coord()
    elif ask =='2':
        port = 'http://api.map.baidu.com/place/v2/search'
        query = 'query=政府机构'
        pages = '&page_size=20&page_num='
        bounds = '&bounds='
        attemp = SEARCH()
        attemp.area()
    else:
        print('Ask again')
        continue


