import urllib.request, urllib.parse, urllib.error
import json
import sqlite3
import csv
from bs4 import BeautifulSoup
import re
import time


##setup csv file
connection = sqlite3.connect('InfoMap.sqlite');
cur = connection.cursor();
cur.executescript('''
DROP TABLE IF EXISTS Map;

CREATE TABLE Map(
    Port_Name TEXT,
    Location TEXT,
    Contact_Person TEXT,
    Telephone TEXT,
    Fax TEXT,
    Address TEXT
)''')

## Define parameters
url = "http://www.wz56.com/workpoints.aspx?page=";
key =0;
print("Searching");
## define the count number

def openurl(link):
    print("Retrieving", link);
    data = urllib.request.urlopen(link,timeout=100);
    sp = BeautifulSoup(data,'html.parser',from_encoding="gb18030");
    return sp;

def readinfopage(address):
    soup = openurl("http://www.wz56.com/"+address);

    body = soup.find('div',attrs={"class":"detailBody"});
    tds = body.find_all('td');

    ##default info
    name=" ";
    location=" ";
    contact=" ";
    phone=" ";
    fax=" ";
    addr=" ";

    ## extract info from the page
    for td in tds:
        ##transform the piece of info into string
        line = "";
        
        for x in td.getText():
            line+=str(x);
        ##iterate info
        if (line.startswith("网点")):
            key =1;
            continue;
        if (key==1):
            key=0;
            name = line;

        if (line.startswith("所在地")):
            key = 2;
            continue;
        if (key==2):
            key=0;
            location = line;

        if (line.startswith("联系人")):
            key = 3;
            continue;
        if (key==3):
            key=0;
            contact = line;

        if (line.startswith("电话")):
            key = 4;
            continue;
        if (key==4):
            key=0;
            phone = line;

        if (line.startswith("传真")):
            key = 5;
            continue;
        if (key==5):
            key=0;
            fax = line;

        if (line.startswith("详细地址")):
            key = 6;
            continue;
        if (key==6):
            key=0;
            addr = line;
    cur.execute("INSERT OR IGNORE INTO Map VALUES(?,?,?,?,?,?)",\
                (name,location,contact,phone,fax,addr))

def readonepage(link):
    soup = openurl(link);
    tds = soup.find_all('td');
    for td in tds:
        href = td.find_all("a");
        if (len(href)>0):
            ## transform the class of the type into string
            line = "";
            for x in href:
                line+=(str(x));
            address = re.findall(r"show.*\d",line)[0];
            if (len(address)>0):
                readinfopage(address);
        connection.commit();


def main():
    for count in range(1,88):
        try:
            print("reading page "+str(count));
            readonepage(url+str(count));
        except:
            print("ending crawler");
    cur.close();
    connection.close();

if __name__=='__main__':
    main()
    
