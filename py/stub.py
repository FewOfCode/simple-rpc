class Adapter(object):

    def __init__(self,server) -> None:
        self.__server = server
        self.method = None
    
    @classmethod
    def register(cls,server):
        return cls(server=server)


    def __call__(self,method:str,*args,**kwargs):
        self.method = method

    
    def is_method_valid(self):
        if self.method.startswith("__"):
            print(f"{self.method} can not start with __")
            return False
        try:
            func = getattr(self.__server,self.method)
        except AttributeError:
            print(f"{self.method} is undefined")
            return False
        if not callable(func):
            print(f"{self.method} is not callable")
        return True

    def is_parameter_valid(self):
        ...

    def is_server_valid(self):
        ...

    