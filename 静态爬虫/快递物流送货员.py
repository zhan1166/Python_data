import urllib.request, urllib.parse, urllib.error
import sqlite3
import csv
import time
from bs4 import BeautifulSoup
import re

##Define parameters
url = "https://www.ickd.cn/outlets/177";

##setup csv file
connection = sqlite3.connect('InfoMap.sqlite');
cur = connection.cursor();
cur.executescript('''
DROP TABLE IF EXISTS Map;
DROP TABLE IF EXISTS Info;

CREATE TABLE Info(
    网点 TEXT,
    名字 TEXT,
    电话 TEXT,
    地址 TEXT
);

CREATE TABLE Map(
    名字 TEXT,
    地址 TEXT,
    联系电话 TEXT,
    派送区域 TEXT,
    不派送区域 TEXT
)''')

def urlreading(link):
    print("Retrieving: ",link);
    uh = urllib.request.urlopen(link,timeout=100);
    sp = BeautifulSoup(uh,'html.parser',from_encoding="gb18030");
    return sp;

def pagereading(link):
    soup = urlreading(link);
    divs = soup.find_all('div',attrs={'class':'outlet-item'});
    for div in divs:
        name = div.find('h3').getText();
        info = div.find('p').getText();
        href = div.find('h3');
        ##extract the hyper link
        line = "";
        for x in href:
            line+=str(x);
        target = "https://www.ickd.cn/outlets/"+line.split('\"')[1];
        ##transfrom soup into string
        Name = "";
        Info = "";
        for x in name:
            Name+=str(x);
        for x in info:
            Info+=str(x);

        soupTarget = urlreading(target);
        try:
            postList = soupTarget.find_all('li',attrs={'class':'postman-item'});
        except:
            print("No message!!!");
            print("The name is: "+Name);
            continue;
        for x in postList:
            content = x.getText();
            #transform to string
            contentStr = "";
            for i in content:
                contentStr+=str(i);
            try:
                postPhone = re.findall("[0-9]{6,12}",contentStr)[0];
                index_phone = contentStr.index(postPhone);
            except:
                print("No phone number!!!");
                print("Name is:"+Name);
                print(contentStr);
                continue;
            
            postName = contentStr[0:index_phone-1];
            postArea = contentStr[index_phone+len(postPhone):];
            cur.execute("INSERT OR IGNORE INTO Info VALUES(?,?,?,?)",\
                        (Name,postName,postPhone,postArea));
        connection.commit();
            
        ##找寻物联网点信息


##        try:
##            index_loc = Info.index("地址");
##        except:
##            index_loc = -1;
##        try:
##            index1_p = Info.index("联系电话");
##        except:
##            index1_p = -1;
##        try:
##            index2_p = Info.index("派送区域");
##        except:
##            index2_p = -1;
##        try:
##            index3_p = Info.index("不派送区域");
##        except:
##            index3_p = -1;
##
##
##        if (index1_p!=-1 and index2_p>0 and index3_p>0 and index2_p<index3_p):
##            phone = Info[index1_p+5:index2_p];
##            openLoc = Info[index2_p+5:index3_p];
##            closeLoc = Info[index3_p+6:];
##            if (index_loc!=-1):
##                location = Info[index_loc+3:index1_p];
##            else:
##                location = " ";
##        elif(index1_p!=-1 and index2_p>0 and index3_p<0):
##            phone = Info[index1_p+5:index2_p];
##            openLoc = Info[index2_p+5:];
##            closeLoc = " ";
##            if (index_loc!=-1):
##                location = Info[index_loc+3:index1_p];
##            else:
##                location = " ";
##        elif(index1_p!=-1 and index3_p>0 and index2_p<0):
##            phone = Info[index1_p+5:index3_p];
##            openLoc = " ";
##            closeLoc = Info[index3_p+6:];
##            if (index_loc!=-1):
##                location = Info[index_loc+3:index1_p];
##            else:
##                location = " ";
##        elif(index1_p!=-1):
##            phone = Info[index1_p+5:];
##            openLoc = " ";
##            closeLoc = " ";
##            if (index_loc!=-1):
##                location = Info[index_loc+3:index1_p];
##            else:
##                location = " ";
##        elif(index1_p==-1 and index2_p>0 and index3_p>0 and index2_p<index3_p):
##            phone = " ";
##            openLoc = Info[index2_p+5:index3_p];
##            closeLoc = Info[index3_p:];
##            if (index_loc!=-1):
##                location = Info[index_loc+3:index2_p];
##            else:
##                location = " ";
##        elif(index1_p==-1 and index2_p==-1 and index3_p>0):
##            phone = " ";
##            openLoc = " ";
##            closeLoc = Info[index3_p:];
##            if (index_loc!=-1):
##                location = Info[index_loc+3:index1_p];
##            else:
##                location = " ";
##        else:
##            phone = " ";
##            openLoc = " ";
##            closeLoc = " ";
##            if (index_loc!=-1):
##                location = Info[index_loc+3:index1_p];
##            else:
##                location = " ";
##        
##        cur.execute("INSERT OR IGNORE INTO Map VALUES(?,?,?,?,?)",\
##                    (Name,location,phone,openLoc,closeLoc));
##        connection.commit();
        
def main():
    for x in range(1,193):
        pagereading(url+"_"+str(x)+".html");
##    cur.close();
##    connection.close();
    
if __name__=='__main__':
    main();
