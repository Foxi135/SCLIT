import sys
import os
import requests
import json
import zipfile
from colorama import Fore, Style, Back, just_fix_windows_console
just_fix_windows_console()
action = sys.argv[1].lower()
if (action == "sui"):
    if (sys.argv[2] == "u")or(sys.argv[2] == "i"):
        if sys.argv[2] == "u":
            x = requests.get("https://sui.sid72020123.repl.co/get_user/"+sys.argv[3])
        if sys.argv[2] == "i":
            x = requests.get("https://sui.sid72020123.repl.co/get_id/"+sys.argv[3])
        x = json.loads(x.text)
        if x["Error"]:
            print("user with "+ Style.BRIGHT +(({"u":"id ","i":"username "})[sys.argv[2]]) + "\"" + sys.argv[3] + "\" " + Style.RESET_ALL + Back.RED + "does not exist" + Style.RESET_ALL)
            quit()
        if sys.argv[2] == "u":
            print(x["Username"])
        if sys.argv[2] == "i":
            print(x["ID"])
    else:
        print("invalid argument: " + Style.BRIGHT + "\""+sys.argv[3]+"\"" + Style.RESET_ALL + ",\nonly "+ Style.BRIGHT + "\"u\""+ Style.RESET_ALL + " (get username) and "+ Style.BRIGHT + "\"i\""+ Style.RESET_ALL +" (get id)")

if (action == "download") or (action == "d"):
    id = sys.argv[2]
    x = json.loads((requests.get("https://api.scratch.mit.edu/projects/"+id)).text)
    try:
        x = x["project_token"]
    except:
        print("project with id " + Style.BRIGHT + id + " " + Style.RESET_ALL + Back.RED + "does not exist" + Style.RESET_ALL)
        quit()
    x = (requests.get("https://projects.scratch.mit.edu/"+id+"?token="+x)).text
    try:
        sys.argv[3]
    except:
        dir = "project"+id
    name = dir+".sb3"
    if not os.path.exists(dir):
        os.mkdir(dir)
        open(dir+"/project.json","w").write(x)
    x = json.loads(x)
    all = 0
    for w in x["targets"]:
        for v in w["costumes"]:
            all = all+1
        for v in w["sounds"]:
            all = all+1
    count = 0
    def progress():
        print(str(round(count/all*100))+"% [" + ("="*round(count/all*20)) + (" "* (20-round(count/all*20))) + "] " + str(count) + "/" + str(all), end="\r")

    for w in x["targets"]:
        for v in w["costumes"]:
            f = requests.get("http://cdn.scratch.mit.edu/internalapi/asset/"+v["md5ext"]+"/get/")
            open(dir+"/"+v["md5ext"],"wb").write(f.content)
            f = None
            count = count+1
            progress()
        for v in w["sounds"]:
            f = requests.get("http://cdn.scratch.mit.edu/internalapi/asset/"+v["md5ext"]+"/get/")
            open(dir+"/"+v["md5ext"],"wb").write(f.content)
            f = None
            count = count+1
            progress()
    if os.path.isfile(name):
        os.remove(name)
    file = zipfile.ZipFile(name,"w")
    for i in os.listdir(dir):
        file.write(dir+"/"+i)
    file.close()
    for i in os.listdir(dir):
        os.remove(dir+"/"+i)
    os.removedirs(dir)
    print("done")

if action == "help":
    print(
"""
d/download ━━ <project id> ━━ <file name (optional)>
sui ━━━━━━━┳━ i (get id) ━━ <username>
           ┗━ u (get username) ━━ <user id>
""")