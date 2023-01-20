local json = require "json"
function run()
	print("Scratch CLI project downloader test made by Foxi135\n\n")
	local action
	if (arg == {})or(arg == nil)or(arg[1] == nil) then
		print("Isn't there an error? program didn't recived any arguments\ntry using \"help\" argument for some info")
	else
		action = string.lower(arg[1] or "")
	end
	if (action == "help") or (action == "--help") then
		local help = {
			"D or DOWNLOAD Download projects, 1 input: project id"
		}
		for k, v in pairs(help) do
			print(v.."\n")
		end
		print("That's everything for now..")
	end
	if (action == "download") or (action == "d") then
		print("--- Downloading project ---")
		local id = arg[2]
		print("creating directory")
		os.execute("@rmdir /q /s project")
		os.execute("@mkdir project")
		print("downloading project api for token")
		local file = http(string.format("https://projects.scratch.mit.edu/%s?token=%s",id,(json.decode(http("https://api.scratch.mit.edu/projects/"..id))).project_token))
		write("project/project.json",file)
		print("decoding json")
		file = (json.decode(file))
		print("downloading assets")
		for k, v in pairs(file.targets) do
			local progress = ""
			local precent = math.ceil((k/#file.targets)*100)
			for i = 1, precent, 1 do
				progress = progress.."#"
			end
			for i = 1, 100-precent, 1 do
				progress = progress.." "
			end
			progress = "["..progress.."] "..tostring(precent).."%"
			os.execute("@cls")
			print("Downloading assets from sprite \""..v.name.."\"\n"..progress)
			print("\n\n\n")
			for k, v in pairs(v.sounds) do
				os.execute(string.format("@powershell wget -o project/%s http://cdn.scratch.mit.edu/internalapi/asset/%s/get/",v.md5ext,v.md5ext))
			end
			for k, v in pairs(v.costumes) do
				os.execute(string.format("@powershell wget -o project/%s http://cdn.scratch.mit.edu/internalapi/asset/%s/get/",v.md5ext,v.md5ext))
			end
		end
		os.execute("@cls")
		print("Copressing project files to .sb3")
		os.execute("@powershell Compress-Archive ./project/* "..id..".zip")
		os.rename(id..".zip",id..".sb3")
		os.execute("@rmdir /q /s project")
		print("All done!")
	end
end
function write(name,content)
	local file = io.open(name, "a")
	file:write(content)
	file:close()
end
function http(url)
	local query = nil
	query = io.popen("curl -s \"" .. url .. "\"", "r")
    local httpsResult = query:read("*all")
    query:close()
    return httpsResult
end
function print(v)
	io.write(v.."\n")
end
run()