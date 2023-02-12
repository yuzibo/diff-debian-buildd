#!/bin/python3

import urllib3
from bs4 import BeautifulSoup
import requests

import re
import json
import datetime

# global directory to store status and it's packages list
package_status = { }

def filter_list(packages_list):
    return [val for val in packages_list
        if re.search(r'package.php?p', val) or re.search(r'Auto-Not-For-Us', val) or
            re.search(r'BD-Uninstallable', val) or re.search(r'Build-Attempted', val) or
            re.search(r'Building',val) or re.search(r'Dep-Wait', val) or
            re.search(r'Failed', val) or re.search(r'Needs-Build', val) or re.search(r'Uploaded', val)]

#  
def loop_packages(packages_list):
    # packages_list[0] is no meaning string
    i = 1
    for i in range(len(packages_list)):
       if packages_list[i] == 'Auto-Not-For-Us':
           package_status['Auto-Not-For-Us'] = packages_list[i-1]
       if packages_list[i] == 'BD-Uninstallable':
           package_status['BD-Uninstallable'] = packages_list[i-1]
       if packages_list[i] == 'Build-Attempted':
           package_status['Build-Attempted'] = packages_list[i-1]
       #if packages_list[i] == 'Building':
       #    package_status['Building'] = packages_list[i-1]
       if packages_list[i] == 'Failed':
           package_status['Failed'] = packages_list[i-1]
       i = i + 1 
    return package_status

# deal with like ['package.php?p=i810switch', 'libsmbios','dials&suite=sid']
# ['package.php?p=i810switch&suite=sid']
def filter_first_and_last(packages_list):
    i = 0
    listed = []
    if len(packages_list) == 1:
            return [(packages_list[0][packages_list[0].find('=')+1:packages_list[0].find('&')])]

    for i in range(len(packages_list)):
        if i == 0:
            listed.append(packages_list[i][packages_list[i].find('=')+1:])
        elif i == (len(packages_list) - 1):
            listed.append(packages_list[i][:packages_list[i].find('&')])
        else:
            listed.append(packages_list[i])
         
        i = i + 1

    return ','.join(sorted(listed))

# split packages name with ',' from str to list
def deal_with_packages(packages_string):
    package_list = re.split(',', packages_string)
    return package_list

def connect_buildd():
    target = 'https://buildd.debian.org/status/architecture.php?a=riscv64&suite=sid'
    req = requests.get(url=target)
    #req.encoding = 'utf-8'
    content = req.text
    #print (content)
    bf = BeautifulSoup(content ,'lxml')
    packages_list = []
    for k in bf.find_all('a'):
        #print(k['href'])
        packages_list.append(k['href'])
        packages_list.append(k.string)
    return packages_list

# deal with dict, which has been stored info
def call_status_list(package_status, file_name):
    for k, v in package_status.items():
        package_status[k] = filter_first_and_last(deal_with_packages(str(v))) 

    # write to file
    #j = json.dumps(package_status)
    with open("data/" + file_name,"w") as file:
            #json.dump(package_status, file)
            file.write(json.dumps(package_status, indent=4, ensure_ascii=False))

if __name__ == '__main__':
    file_name = datetime.datetime.now().strftime("%Y-%m-%d") + '.json'
    packages_list = connect_buildd()
    packages_list = filter_list(packages_list)
    package_status = loop_packages(packages_list)
    print ("==== Ready for generating --------------\n")
    call_status_list(package_status, file_name)
    print ("==== Done --------------\n")
