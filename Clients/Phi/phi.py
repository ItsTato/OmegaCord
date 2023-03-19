import socket, threading, os
from json import loads, dumps
from requests import get

def clearConsole():
	os.system("cls" if os.name in ["nt"] else "clear")

if __name__ != "__main__":
	exit()

addr:str = input("IP: ")

#ip = ip.replace("tcp://","")
#ip = ip.replace("http://","")
#ip = ip.replace("https://","")

print("Attempting to get socket fqdn...")

sockFqdn:str = get(f"{addr}/api/socket/fqdn").text

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
except:
	print("Connection failed!")
	exit(0)

print("Connected!")

clearConsole()

username:str = input("Join as: ")

soc.send(username.encode("utf-8"))

clearConsole()

def recv():
	while True:
		msg = soc.recv(1024).decode("utf-8")
		print(f"\n{msg}")

recvThread = threading.Thread(target=recv)
recvThread.setDaemon(True)
recvThread.start()

running:bool = True

prefix = f"{username}@{sockIp}"

while running:
	cmd = input(f"{prefix}> ")
	if cmd.lower() in ["end"]:
		soc.close
		running = False
		exit(0)
	if cmd.lower() in ["send", "msg"]:
		msg = input(f"{prefix}$msg> ")
		soc.send(str(msg).encode("utf-8"))

soc.close()
