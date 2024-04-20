import os

def clear_console() -> None:
	os.system("cls" if os.name in ["nt","dos"] else "clear")
	return