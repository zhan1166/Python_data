from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import requests
import time
from bs4 import BeautifulSoup
import re

##parameters
weblink = [];

####需要下载selenium和chromedrivedriver 安装包
option = webdriver.ChromeOptions();
option.add_argument("disable-infobars");
option.add_argument("--headless");

##chromedriver.exe地址 and 网址
path = r"C:\Users\user\AppData\Local\Google\Chrome\Application\chromedriver\chromedriver.exe";
driver = webdriver.Chrome(executable_path = path, chrome_options = option);
driver.get("http://www.yellowpage.com.cn/ypm/edt/list.html?p=1&c=0D0300000000X2");
driver.maximize_window();
time.sleep(2);

##为了点出温州。。。。。玄学
##——————————————————————————————————————————
actions = ActionChains(driver);
##actions.move_to_element(driver.find_element_by_id("addr_box"));
actions.move_to_element(driver.find_element_by_xpath("//div[@class='add']"));
actions.click();
actions.move_to_element(driver.find_element(By.XPATH, '//*[text()="浙江"]'));
time.sleep(2);
##actions.move_to_element(driver.find_element(By.XPATH, '//div[text()="温州市"]'));
actions.move_by_offset(0,40);
actions.move_by_offset(-230,0);
actions.click();
actions.perform();
time.sleep(2);
##——————————————————————————————————————————

##再次登上黄页网址
driver.get("http://www.yellowpage.com.cn/ypm/edt/list.html?p=1&c=0D0300000000X2");
driver.maximize_window();
time.sleep(2);
##读取数据
content = driver.page_source;
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
        weblink.append("http://www.yellowpage.com.cn/ypm/edt/list_details.html?id="\
                       +result);
    except:
        pass;
        
print(weblink);


##path = r"C:\Users\user\AppData\Local\Google\Chrome\Application\chromedriver\chromedriver.exe";
##driver = webdriver.Chrome(executable_path = path)  # Optional argument, if not specified will search path.
##driver.get('http://www.google.com/xhtml');
##time.sleep(5) # Let the user actually see something!
##search_box = driver.find_element_by_name('q')
##search_box.send_keys('ChromeDriver')
##search_box.submit()
##time.sleep(5) # Let the user actually see something!
##driver.quit()
