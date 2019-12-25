import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup

##Parameters
key =0;
url = "http://tongda.wz56.com/showpoint.aspx?id=2719";

data = urllib.request.urlopen(url);
soup = BeautifulSoup(data,'html.parser',from_encoding="gb18030");
body = soup.find('div',attrs={"class":"detailBody"});
tds = body.find_all('td');
## extract info from the page
for td in tds:
    ##transform the piece of info into string
    line = "";
    for x in td.getText():
        line+=str(x);
    if (line.startswith("网点")):
        key =1;
        continue;
    if (key==1):
        key=0;
        print("Name",line);

    if (line.startswith("所在地")):
        key = 2;
        continue;
    if (key==2):
        key=0;
        print("Location",line);

    if (line.startswith("联系人")):
        key = 3;
        continue;
    if (key==3):
        key=0;
        print("Contact Person",line);

    if (line.startswith("电话")):
        key = 4;
        continue;
    if (key==4):
        key=0;
        print("Telephone",line);

    if (line.startswith("传真")):
        key = 5;
        continue;
    if (key==5):
        key=0;
        print("Fax",line);

    if (line.startswith("详细地址")):
        key = 6;
        continue;
    if (key==6):
        key=0;
        print("Address",line);


