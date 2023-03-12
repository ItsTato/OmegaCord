import socket, threading, os

def clearConsole():
	os.system("cls" if os.name in ["nt"] else "clear")

clearConsole()

host:str = "127.0.0.1"
port:int = 6002 # - 6100

soc:socket.socket = socket.socket(socket.AF_INET)

soc.bind((host,port))
print(f"Server listening on {host}:{port}")

soc.listen(100)

clients = {}

running:bool = True

def ctrl():
	while True:
		cmd = input("@psi> ")
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

def sendAll(toSend):
	for client in clients:
		try:
			clients[client]["soc"].send(str(toSend).encode("utf-8"))
		except:
			clients.pop(client)

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

mainThread = threading.Thread(target=main)
mainThread.setDaemon(True)
mainThread.start()

ctrl()
