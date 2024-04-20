from colorama import Fore, Back, Style

from .Clear import clear_console

def ask_for(what:str,options:list[str]=None,default=None,can_be_empty:bool=False,can_be_any:bool=False,invalid_msg:str="Invalid answer! Please try again.") -> str:
	clear_console()
	options_string:str = ""
	if options is not None:
		options_string = " ["
		for index, option in enumerate(options):
			if index == 0:
				options_string = f"{options_string}{option}"
				continue
			options_string = f"{options_string}/{option}"
		options_string = f"{options_string}]"
	default_string:str = ""
	if default is not None:
		default_string = f" ({default})"
	print("")
	while True:
		to_return = input(f"{Fore.LIGHTMAGENTA_EX}{Style.BRIGHT}{what}{Fore.RESET}{Style.RESET_ALL}{options_string}{default_string}: ")
		if default is not None:
			if to_return.replace(" ","") == "":
				return default
		elif options is not None:
			if to_return in options or to_return.lower() in options or to_return.upper() in options:
				return to_return
		elif options is None:
			if to_return.replace(" ","") == "" and can_be_empty:
				return to_return
			if to_return.replace(" ","") != "":
				return to_return
		if can_be_any:
			return to_return
		clear_console()
		print(f"{Back.LIGHTRED_EX}{Style.BRIGHT} ERROR: {Style.RESET_ALL}{Back.RESET} {invalid_msg}")