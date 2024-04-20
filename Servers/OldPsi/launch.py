from os import system, name, path

def clearConsole():
    system("cls" if name in ["nt"] else "clear")

def safeImport(pack, packPypi: str = None):
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

clearConsole()

print("Launching sequence completed!\nInitializing server...")

proj_dir:str = path.dirname(path.realpath(__file__))

if name == "nt":
	system(f"py -3 \"{proj_dir}\\server.py\"")
else:
	system(f"python3 \"{proj_dir}/server.py\"")
