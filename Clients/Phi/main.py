import colorama

from OmegaTools import clear_console, ask_for

colorama.init()

server_protocol:str = ask_for("SERVER PROTOCOL",options=["HTTP","HTTPS"],invalid_msg="Invalid protocol! Please try again.").lower()
server_ip_address:str = ask_for("SERVER IP",invalid_msg="Please enter an IP.")
if not ":" in server_ip_address:
	server_port:str = ask_for("SERVER PORT",default=3002,can_be_any=True,invalid_msg="Invalid port! Please try again.")
	server_address:str = f"{server_protocol}://{server_ip_address}:{server_port}"
else:
	server_address:str = f"{server_protocol}://{server_ip_address}"


