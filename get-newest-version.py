#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import pyquery
mainVersion = int(sys.argv[1])
programVersionList = pyquery.PyQuery(url=f"https://www.kernel.org/")
#release = pyquery.PyQuery()
temp = 0
newestVersion = "0.0.0"
newestUrl = ""
for i in programVersionList(f"#releases tr :nth-child(2)").items():
    version = i("td strong").text()
    if temp == mainVersion:
        #print(version)
        newestVersion = version
        break
    temp += 1

temp = 0
for i in programVersionList(f"#releases tr :nth-child(4)").items():
    url = i("td a").attr.href
    if temp == mainVersion:
        newestUrl = url
        break
    temp += 1


print(f"Version:{newestVersion}")
print(f"Url:{newestUrl}")


if mainVersion == 0: # mainline 
    with open("/tmp/mainline.txt", "w") as file:
        file.write(newestVersion)
    with open("/tmp/mainlineurl.txt", "w") as file:
        file.write(newestUrl)
elif mainVersion == 1: # stable
    with open("/tmp/stable.txt", "w") as file:
        file.write(newestVersion)
    with open("/tmp/stableurl.txt", "w") as file:
        file.write(newestUrl)
elif mainVersion == 2: # longterm
    with open("/tmp/longterm.txt", "w") as file:
        file.write(newestVersion)
    with open("/tmp/longtermurl.txt", "w") as file:
        file.write(newestUrl)
