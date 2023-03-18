import eventlet
eventlet.monkey_patch()

#import socket
from eventlet.green import socket

import threading, os, sqlite3, json
from flask import Flask

def clearConsole():
	os.system("cls" if os.name in ["nt"] else "clear")

clearConsole()

config = {}
if os.path.exists("./config.json"):
	with open("./config.json","r") as f:
		config = json.load(f)
		f.close()
else:
	print(f"Server could not find config.json configuration file!")
	exit()

try:
	socketHost:str = config["SOCKET"]["HOST"]
	socketPort:int = config["SOCKET"]["PORT"]
	socketFqdn:str = config["SOCKET"]["FQDN"]

	webHost:str = config["WEB"]["HOST"]
	webPort:int = config["WEB"]["PORT"]
	webFqdn:str = config["WEB"]["FQDN"]
except:
	print("Configuration file (./config.json) was not loaded successfully.\nIs it corrupted?")
	exit()

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
app = Flask(__name__.split(".")[0])

try:
	if config["DATABASE"]["LOCAL_FILE"] == True:
		database = sqlite3.connect(f"{config['DATABASE']['URI']}")
		print("Server connected to local file database")
	elif config["DATABASE"]["LOCAL_FILE"] == False:
		database = sqlite3.connect(f"{config['DATABASE']['URI']}")
		print("Server connected to external database")
	else:
		print("What did you even do???")
except:
	print("Server could not connect to database!")
	exit()

try:
	soc.bind((socketHost,socketPort))
	soc.listen(128)
	print(f"Server socket now listening on {socketHost}:{socketPort}")
except:
	print(f"Server socket could not bind to {socketHost}:{socketPort}!\nPerhaps the IP is invalid?\nPerhaps the port is already in use?")
	exit()

def doesTableExist(tableName):
	cur = database.cursor()
	return False if len(cur.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{tableName}';").fetchall()) == 0 else True

@app.route("/",methods=["GET"])
def root():
	return f"Welcome to your <a href=\"https://github.com/ItsTato/OmegaCord\">OmegaCord</a> Psi (v{config['VER']}) server!"

clients:dict = {}
running:bool = True

def sendAll(toSend):
	for client in clients:
		try:
			clients[client]["soc"].send(str(toSend).encode("utf-8"))
		except:
			sendAll(f"User {clients[client]['user']} has left.")
			clients[client]["soc"].close()
			clients.pop(client)
			continue

def recv(soc,addr,user):
	while True:
		try:
			msg = soc.recv(1024).decode("utf-8")
			if str(msg).replace(" ","") != "":
				sendAll(f"{user}: {msg}")
		except:
			pass

def main():
	while running == True:
		com_soc,address = soc.accept()
		user = com_soc.recv(1024).decode("utf-8")
		data = {"soc": com_soc, "addr": address, "user": user}
		clients[address] = data
		recvThread = threading.Thread(target=recv,args=(com_soc,address,user))
		recvThread.setDaemon(True)
		recvThread.start()

def web():
	import eventlet
	from eventlet import wsgi
	wsgi.server(eventlet.listen((webHost,webPort)),app)
	#app.run(host=webHost,port=webPort,debug=False)

mainThread = threading.Thread(target=main)
webThread = threading.Thread(target=web)
mainThread.setDaemon(True)
webThread.setDaemon(True)
mainThread.start()
webThread.start()

def ctrl():
	while True:
		cmd = input(f"Psi-v{config['VER']}@OmegaCord> ")
		if cmd.lower() in ["stop","end"]:
			print("Disconnecting clients...")
			for client in clients:
				try:
					clients[client]["soc"].close()
				except:
					pass
			running = False
			print("Server closed.")
			exit(0)

ctrl()
