#35
#http://asteroidsathome.net/boinc/stats/
#FULL CODE: ASTEROIDS DOWNLOAD, PARSE XML, WRITE AND READ CSV

#CONSTANTS
TEAMID="35"
PURL="http://asteroidsathome.net/boinc/stats/"
PNAME="asteroids"
CSVNAME="asteroids100.csv"
#BURP HAS USER_ID.GIZ INSTEAD OF USER.GZ
USERGZ="user"

#DOWNLOAD ASTEROIDS/USER.GZ
import xml.etree.cElementTree as ET
import requests
import gzip
import shutil
import csv

from pprint import pprint

url2 = PURL+"user.gz"
file_name2 = USERGZ
file_ext = '.gz'
target_path2 = file_name2 + file_ext

print('downloading ' + url2)

response = requests.get(url2, stream=True)
if response.status_code == 200:
    with open(target_path2, 'wb') as f:
        f.write(response.raw.read())

#print('file has been downloaded')
#print("")

#EXTRACT USER.XML FROM USER.GZ

#print('extracting ' + str(target_path2))

x_file_name2 = file_name2 + '.xml'
with gzip.open(target_path2, 'rb') as f_in:
    with open(x_file_name2, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

print(str(x_file_name2) + ' extracted')
#print("")

#PARSE XML FILE FOR UBT MEMBERS

tid=0
tc=0
ac=0
cnt=1
ncnt=1
name="none"
id=99999999
cpid="none"
dic={}
print("parsing user.xml")
#print("building nested dictionary")
for event, elem in ET.iterparse("user.xml", events=("start","end")):

    if elem.tag == "total_credit" and event == "end":
        tc=float(elem.text)
        elem.clear

    if elem.tag == "expavg_credit" and event == "end":
        ac=float(elem.text)
        elem.clear

    if elem.tag == "id" and event == "end":
        id=elem.text
        elem.clear

    if elem.tag == "cpid" and event == "end":
        cpid=elem.text
        elem.clear

    if elem.tag == "name" and event == "end":
        name = elem.text
        elem.clear()
    teamid=TEAMID

    if elem.tag == "teamid" and event == "end":
        if elem.text == TEAMID:
            cnt=cnt+1
            dic[id]={"Name":name,"CPID":cpid, "TC":tc, "AC":ac}
        elem.clear()
#print("user.xml parsed")
#print("nested dictionary built")
#print("")
print("total members: " + str(cnt))
#print("")

#print("sorting dictionary on credit")
res = sorted(dic.items(), key = lambda x: x[1]['TC'], reverse=True)
#print("dictionary sorted on credit")
#print("")

#print("building ubt "+PNAME+" top100")
#print("writing top100 csv file")
loopcnt=0
cname=""
cpoints=0
cposition=0
ccpid=""
ccredit=0
crac=0

#WRITE CSV FILE
with open(CSVNAME, 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile)
    spamwriter.writerow(["Position", "Points", "Name", "CPID", "TCredit", "ACredit"])

for k, v in res:
    if(loopcnt == 100):
        break
    loopcnt=loopcnt+1
    #print("")
    #print("position: " + str(loopcnt))
    cposition=str(loopcnt)
    points=(101-loopcnt)
    cpoints=str(points)
    #print("points: "+str(points))

    for key in v:
        if(key == "Name"):
            #print("name: "+str(v[key]))
            cname=str(v[key])
        if (key == "CPID"):
            #print("cpid: " + str(v[key]))
            ccpid=str(v[key])
        if(key == "TC"):
            #print("credit: "+str(v[key]))
            ccredit=str(v[key])
        if (key == "AC"):
            #print("rac: " + str(v[key]))
            crac=str(v[key])

    # WRITE DYNAMIC PART OF CSV FILE

    with open(CSVNAME, 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile)
        spamwriter.writerow([cposition, cpoints, cname, ccpid, ccredit, crac])

print("csv file written")