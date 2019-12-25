import urllib.request, urllib.parse, urllib.error
import sqlite3
from bs4 import BeautifulSoup
import re
import time
import json
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

cur.executescript('''
DROP TABLE IF EXISTS Map;

CREATE TABLE Map(
    Company Name TEXT,
    Phone TEXT,
    Location TEXT
)''')


class YellowPageSearch(object):
    ## url address and weblink list
    url = '';
    weblink = [];
    ####需要下载selenium和chromedrivedriver 安装包
    option = webdriver.ChromeOptions();
    ##chromedriver.exe地址 and 网址
    path = r"C:\Users\user\AppData\Local\Google\Chrome\Application\chromedriver\chromedriver.exe";
    driver = webdriver.Chrome(executable_path = path, chrome_options = option);
    ##page count
    count = 0;
    ##setup csv file
    connection = sqlite3.connect('yellowPage.sqlite');
    cur = connection.cursor();
    

    def __init__(self):
        self.option.add_argument("disable-infobars");
        self.option.add_argument("--headless");
        cur.executescript('''
        DROP TABLE IF EXISTS Map;

        CREATE TABLE Map(
            Company Name TEXT,
            Phone TEXT,
            Location TEXT
        )''')
        
    def urlsetting(self):
        self.count+=1;
        self.url = "http://www.yellowpage.com.cn/ypm/edt/list.html?p="+str(self.count)+"&c=0D0300000000X2";
        print("Retrieving", self.url);

    def driversetup(self):
        self.driver.get(self.url);
        self.driver.maximize_window();

    def ip_address_setup(self):

        ## actions setup
        actions = ActionChains(self.driver);
        ##actions.move_to_element(driver.find_element_by_id("addr_box"));
        actions.move_to_element(self.driver.find_element_by_xpath("//div[@class='add']"));
        actions.click();
        actions.move_to_element(self.driver.find_element(By.XPATH, '//*[text()="浙江"]'));
        time.sleep(2);
        ##actions.move_to_element(driver.find_element(By.XPATH, '//div[text()="温州市"]'));
        actions.move_by_offset(0,40);
        actions.move_by_offset(-230,0);
        actions.click();
        actions.perform();
        time.sleep(2);

    def readonepage(self,link):
        self.driver.get(link);
        self.driver.maximize_window();
        time.sleep(2);
        content = self.driver.page_source;
        soup = BeautifulSoup(content,"html.parser");
        companylist = soup.find_all("div",attrs={"class":"listcontent"});
        for company in companylist:
            ## transfrom into string
            code = company['onclick'];
            line = "";
            for x in code:
                line+=str(x);
            try:
                result = re.findall('\\(.*\\)',line)[0];
                result = result.replace('(','').replace(')','').strip('\\"');
                self.weblink.append("http://www.yellowpage.com.cn/ypm/edt/list_details.html?id="\
                               +result);
            except:
                pass;

    def read_company_info(self):
        

    def main(self):
        self.urlsetting();
        self.driversetup();
        self.ip_address_setup();
        for x in range(0,20):
            self.readonepage(self.url);
            self.urlsetting();
        print(self.weblink);

if __name__=='__main__':
    Program = YellowPageSearch();
    Program.main();







        
