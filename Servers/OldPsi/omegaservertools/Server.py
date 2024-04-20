class Server:
	def __init__(self,id:int,name:str,icon_url:str,channels:dict,members:list) -> None:
		self.ID:int = id
		self.NAME:str = name
		self.ICON_URL:str = icon_url
		self.CHANNELS:dict = channels