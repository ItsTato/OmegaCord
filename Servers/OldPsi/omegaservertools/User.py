class User:
    def __init__(self,id:int,username:str,tag:int,displayname:str,severs:dict,friends:dict,pms:dict) -> None:
        self.ID:int = id
        self.USERNAME:str = username
        self.TAG:int = tag
        self.DISPLAYNAME:str = displayname
        self.SERVERS:dict = severs
        self.FRIENDS:dict = friends
        self.PMS:dict = pms