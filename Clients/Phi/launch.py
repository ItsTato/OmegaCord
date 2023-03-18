from os import system, name

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

gitVer = requests.get("https://raw.githubusercontent.com/ItsTato/OmegaCord/master/Clients/Phi/phi.py").text

if not gitVer == full:
	print("Update available! Applying...")
	with open("./phi.py","w") as f:
		f.write(gitVer)
		f.close()
	print("Phi updated successfully!")

print("Alls good! Launching Phi...")
print("-"*30)

if name == "nt":
	system("py -3 \"./phi.py\"")
else:
	system("python3 \"/phi.py\"")
