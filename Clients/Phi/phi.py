import socket, threading, os
from json import loads, dumps

def clearConsole():
	os.system("cls" if os.name in ["nt"] else "clear")

if __name__ != "__main__":
	exit()

clearConsole()

ip:str = input("IP: ")

if ":" in ip:
	port = ip.split(":")[1]
	ip = ip.split(":")[0]
else:
	port:int = input("AT: ")

print("Connecting...")

soc  = socket.socket(socket.AF_INET)
try:
	soc.connect((ip,int(port)))
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

prefix = f"{username}@{ip}"

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
