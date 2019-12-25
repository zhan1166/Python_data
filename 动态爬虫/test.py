import re

string = '<div class="listcontent" onclick="godetas("c9fe7ecb-ac72-11e6-933e-6c3be5ab01702064235")"><div class="firmname">吉通速递有限公司</div><div style="clear:both;"></div><div class="jyfw"><img src="ypImgs/list/erweima.png" style="height: 18px;padding: 4px 10px 1px 0px;float: left;"/></div><div class="jyfw1">物流业<div style="float:right;"><img src="ypImgs/list/addicon.png"\
style="float:left;width:15px;"/><div style="float:left;"> 平阳县</div></div></div></div>';

result = re.findall('\\(.*\\)',string)[0];
result = result.replace('(','').replace(')','').strip('\\"');
print(result);
