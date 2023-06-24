import socket, threading, os
from requests import get

def clearConsole():
	os.system("cls" if os.name in ["nt"] else "clear")

if __name__ != "__main__":
	exit()

gettingProtocol:bool = True

while gettingProtocol:
	serverProtocol:str = input("PROTOCOL [HTTP/HTTPS]: ").lower()
	if serverProtocol in ["http","https"]:
		gettingProtocol = False
	else:
		print("Invalid protocol! Please try again:")
serverIp:str = input("IP: ")

if not ":" in serverIp:
	serverPort:str = input("PORT (3002): ")
	if serverPort in [""," "]:
		serverPort = 3002
	serverPort:int = serverPort
	serverAddress:str = f"{serverProtocol}://{serverIp}:{serverPort}"
else:
	serverAddress:str = f"{serverProtocol}://{serverIp}"

print("Attempting to get socket fqdn...")

toUse:str = ""
if serverAddress.endswith("/"):
	toUse = f"{serverAddress}api/socket/fqdn"
else:
	toUse = f"{serverAddress}/api/socket/fqdn"

sockFqdn:str = get(f"{toUse}").text

sockFqdn = sockFqdn.replace("tcp://","")
sockFqdn = sockFqdn.replace("http://","")
sockFqdn = sockFqdn.replace("https://","")

if ":" in sockFqdn:
	sp = sockFqdn.split(":")
	sockIp = sockFqdn.split(":")[0]
	sockPort = sockFqdn.split(":")[1]
else:
	sockIp = sockFqdn
	sockPort = 6002

print(f"Connecting to {sockIp} @ {sockPort}...")

soc  = socket.socket(socket.AF_INET)
try:
	soc.connect((sockIp,int(sockPort)))
except Exception as e:
	print("Connection failed!")
	exit(0)

print("Connected!")

clearConsole()

username:str = input("Join as: ")

soc.send(username.encode("utf-8"))

clearConsole()

safeForNoNewLine:bool = True

def recv():
	while True:
		receivedMsg = soc.recv(1024).decode("utf-8")
		if safeForNoNewLine:
			print(f"{receivedMsg}")
		else:
			print(f"\n{receivedMsg}")

recvThread = threading.Thread(target=recv)
recvThread.daemon = True
recvThread.start()

running:bool = True

prefix = f"{username}@{sockIp}"

while running:
	cmd = input(f"{prefix}> ")
	if cmd.lower() in ["end","disconnect","leave"]:
		soc.close()
		running = False
		exit(0)
	if cmd.lower() in ["send", "msg"]:
		msg = input(f"{prefix}$msg> ")
		soc.send(str(msg).encode("utf-8"))

soc.close()
