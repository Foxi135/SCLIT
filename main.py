import sys
import os
import requests
import json
import zipfile
action = sys.argv[1]
if (action == "sui"):
    if (sys.argv[2] == "u")or(sys.argv[2] == "i"):
        if sys.argv[2] == "u":
            x = requests.get("https://sui.sid72020123.repl.co/get_user/"+sys.argv[3])
        if sys.argv[2] == "i":
            x = requests.get("https://sui.sid72020123.repl.co/get_id/"+sys.argv[3])
        x = json.loads(x.text)
        if sys.argv[2] == "u":
            print(x["Username"])
        if sys.argv[2] == "i":
            print(x["ID"])
    else:
        print("invalid argument: \""+sys.argv[2]+"\"")

if (action == "download") or (action == "d"):
    id = sys.argv[2]
    x = json.loads((requests.get("https://api.scratch.mit.edu/projects/"+id)).text)
    x = x["project_token"]
    x = (requests.get("https://projects.scratch.mit.edu/"+id+"?token="+x)).text
    dir = "project"+id
    if not os.path.exists(dir):
        os.mkdir(dir)
        open(dir+"/project.json","w").write(x)
    x = json.loads(x)
    for w in x["targets"]:
        for v in w["costumes"]:
            print(v)
            f = requests.get("http://cdn.scratch.mit.edu/internalapi/asset/"+v["md5ext"]+"/get/")
            open(dir+"/"+v["md5ext"],"wb").write(f.content)
            f = None
        for v in w["sounds"]:
            print(v)
            f = requests.get("http://cdn.scratch.mit.edu/internalapi/asset/"+v["md5ext"]+"/get/")
            open(dir+"/"+v["md5ext"],"wb").write(f.content)
            f = None

