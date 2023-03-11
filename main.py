import sys
import os
import requests
import json
import zipfile
import datetime
from colorama import Fore, Style, Back, just_fix_windows_console
just_fix_windows_console()

try:
    action = sys.argv[1].lower()
except:
    print("next time do \"sclit help\"")
    quit()
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
    token = False
    try:
        token = sys.argv[sys.argv.index("token:")+1]
    except:
        token = False
    if not token:
        try:
            newline = "\n"
            date = datetime.datetime.now()
            try:
                d = x["description"]
                d = None
            except:
                x["description"] = ""
            try:
                d = x["instructions"]
                d = None
            except:
                x["instructions"] = ""
            info = f'date of download: {date.year}-{date.month}-{date.day} {date.hour}:{date.minute} {newline}project name: {x["title"]} {newline}created by: {x["author"]["username"]} {newline}project id: {x["id"]} {newline}date of creation: {x["history"]["created"]} {newline}shared: {x["history"]["shared"]} {newline}Instructions:{newline}{x["instructions"]}{newline}Notes and credits (description):{newline}{x["description"]}{newline}{newline}Downloaded with SCLIT by Foxi135'
            date = None
            title = x["title"]
            x = x["project_token"]
        except:
            try:
                u = sys.argv[sys.argv.index("json-url:")+1]
                u = None
                newline = "\n"
                date = datetime.datetime.now()
                info = f'date of download: {date.year}-{date.month}-{date.day} {date.hour}:{date.minute} {newline}Downloaded with SCLIT by Foxi135'
                date = None
            except:
                print("project with id " + Style.BRIGHT + id + " " + Style.RESET_ALL + Back.RED + "does not exist" + Style.RESET_ALL)
                quit()
    else:
        x = token
        token = None
    try:
        dir = sys.argv[sys.argv.index("name:")+1]
        if dir == "?":
            dir = title
        for char in (["\\","/",":","*","\"","<",">","|","?"]):
            dir = dir.replace(char, "_")
        name = dir+".sb3"
        dir = "project"+id+" - "+name
    except:
        dir = "project"+id
        name = dir+".sb3"
    try:
        x = sys.argv[sys.argv.index("json-url:")+1]
        x = (requests.get(x)).text
    except:
        x = (requests.get("https://projects.scratch.mit.edu/"+id+"?token="+x)).text
    x = json.loads(x)
    if not os.path.exists(dir):
        os.mkdir(dir)
        x["targets"][1]["comments"]["SCLIT-credit"] = {"blockId":None,"x":300,"y":300,"width":200,"height":200,"minimized":False,"text":info}
        open(dir+"/project.json","w").write(json.dumps(x))
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
d/download ━━ <project id> ━━ name: <file name or ? to get project title> (optional) ━━ token: <token> (optional) ━━ json-url: <json-url> (optional)

sui ━━━━━━━┳━ i (get id) ━━━━━━━━ <username>
           ┗━ u (get username) ━━ <user id>

examples: 
sclit d 817400236 name: ?
sclit sui i Foxi135

created by Foxi135
""")