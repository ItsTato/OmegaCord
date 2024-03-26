import socket, threading, os, sqlite3, json, colorama

colorama.init()

def clearConsole():
	os.system("cls" if os.name in ["nt"] else "clear")

proj_dir: str = os.path.dirname(os.path.realpath(__file__))

clearConsole()

config = {}
if os.path.exists(f"{proj_dir}/config.json"):
	with open(f"{proj_dir}/config.json", "r") as f:
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

soc = socket.socket(socket.AF_INET)

try:
	if config["DATABASE"]["LOCAL_FILE"]:
		database = sqlite3.connect(f"{proj_dir}/{config['DATABASE']['URI']}")
		print("Server connected to local file database")
	elif not config["DATABASE"]["LOCAL_FILE"]:
		database = sqlite3.connect(f"{config['DATABASE']['URI']}")
		print("Server connected to external database")
	else:
		print("What did you even do???")
except:
	print("Server could not connect to database!")
	exit()

def doesTableExist(tableName):
	cur = database.cursor()
	return False if len(cur.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{tableName}';").fetchall()) == 0 else True

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

def recv(passedSocket,addr,user):
	while True:
		try:
			msg = passedSocket.recv(1024).decode("utf-8")
			if str(msg).replace(" ","") != "":
				sendAll(f"{user}: {msg}")
		except:
			pass

def main():
	try:
		soc.bind((socketHost,socketPort))
		soc.listen(128)
		print(f"Server socket now listening on {socketHost}:{socketPort}")
	except:
		print(f"Server socket could not bind to {socketHost}:{socketPort}!\nPerhaps the IP is invalid?\nPerhaps the port is already in use?")
		exit()
	while running == True:
		com_soc,address = soc.accept()
		user = com_soc.recv(1024).decode("utf-8")
		data = {"soc": com_soc, "addr": address, "user": user}
		clients[address] = data
		recvThread = threading.Thread(target=recv,args=(com_soc,address,user))
		recvThread.daemon = True
		recvThread.start()

def web():
	from flask import Flask

	app = Flask(__name__.split(".")[0])

	@app.route("/",methods=["GET"])
	def home():
		return f"Welcome to your <a href=\"https://github.com/ItsTato/OmegaCord\">OmegaCord</a> Psi (v{config['VER']}) server!"
	
	@app.route("/api/socket/fqdn",methods=["GET"])
	def apiSocket():
		return str(socketFqdn)

	app.run(host=webHost,port=webPort,debug=False)

mainThread = threading.Thread(target=main)
webThread = threading.Thread(target=web)
mainThread.daemon = True
webThread.daemon = True
if __name__ == "__main__":
	mainThread.start()
	webThread.start()
	def ctrl():
		while True:
			cmd = input(
				f"{colorama.Fore.RESET}{colorama.Style.RESET_ALL}{colorama.Back.RESET}{socket.gethostname()}{colorama.Fore.LIGHTYELLOW_EX}{colorama.Style.BRIGHT}@{colorama.Style.RESET_ALL}{colorama.Fore.RESET}Psi-v{config['VER']} {colorama.Fore.LIGHTYELLOW_EX}{colorama.Style.BRIGHT}~ {colorama.Fore.RESET}{colorama.Style.RESET_ALL}{colorama.Back.RESET}").lower()
			if cmd in ["stop","end"]:
				print("Disconnecting clients...")
				for client in clients:
					try:
						clients[client]["soc"].close()
					except:
						pass
				global running
				running = False
				print("Server closed.")
				exit(0)
			if cmd in ["cls","clear"]:
				os.system("cls" if os.name in ["nt"] else "clear")

	ctrl()
