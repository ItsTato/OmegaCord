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
safeImport("flask")
safeImport("eventlet")

clearConsole()

print("Launching sequence completed!\nInitializing server...")

if name == "nt":
	system("py -3 \"./server.py\"")
else:
	system("python3 \"/server.py\"")
