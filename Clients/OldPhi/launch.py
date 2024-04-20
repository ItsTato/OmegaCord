from os import system, name, rename, remove
from filecmp import cmp

def clearConsole():
	system("cls" if name in ["nt"] else "clear")

def safeImport(pack,packPypi:str=None):
	if packPypi == None:
		packPypi = pack
	if name == "nt":
		try:
			exec(f"import {pack}")
		except:
			system(f"py -3 -m pip install {packPypi}")
	else:
		try:
			exec(f"import {pack}")
		except:
			system(f"python3 -m pip install {packPypi}")

safeImport("requests")
safeImport("colorama")

clearConsole()

print("Checking for updates...")

full = ""
file = []
with open("./phi.py","r") as f:
	file = f.readlines()
	f.close()

for i in range(len(file)):
	if full == "":
		full = f"{file[i]}"
		continue
	full = f"{full}\n{file[i]}"

import requests

phiGitVer = requests.get("https://raw.githubusercontent.com/ItsTato/OmegaCord/master/Clients/Phi/phi.py").text
launcherGitVer = requests.get("https://raw.githubusercontent.com/ItsTato/OmegaCord/master/Clients/Phi/launch.py").text

with open("./tmp.py","w") as f:
	f.write(phiGitVer)
	f.close()

if not cmp("./phi.py","./tmp.py"):
	print("Update available!")
	yn = input("Do you wish to update (Y/n)? ")
	if yn.lower().replace(" ","") in ["y","yes",""]:
		print("Updating...")
		remove("./phi.py")
		rename("./tmp.py","phi.py")
		print("Update applied successfully!")
	else:
		remove("./tmp.py")
else:
	remove("./tmp.py")

with open("./tmp.py","w") as f:
	f.write(launcherGitVer)
	f.close()

if not cmp("./launch.py","./tmp.py"):
	print("Launcher update availalble!")
	yn = input("Do you wish to update the launcher (Y/n)? ")
	if yn.lower().replace(" ","") in ["y","yes",""]:
		remove("./launch.py")
		rename("./tmp.py","launch.py")
		print("Launcher updated!\nPlease re-run this script.")
		exit()
	else:
		remove("./tmp.py")
else:
	remove("./tmp.py")

print("Alright! Alls good! Launching OldPhi...")
print("-"*30)

if name == "nt":
	system("py -3 \"./phi.py\"")
else:
	system("python3 \"/phi.py\"")
