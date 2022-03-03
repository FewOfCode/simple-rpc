
import json,os
from mimetypes import guess_type
class Adapter(object):

    def __init__(self,server,protocol) -> None:
        self.__server = server
        self.method = None
        if os.path.isfile(protocol):
            try:
                with open(protocol,"r",encoding="utf-8") as f:
                    self.protocol = json.load(fp=f)
            except json.JSONDecodeError:
                raise AttributeError(F"protocol content is valid")
            assert self.is_protocol_valid()
        else:
            raise FileNotFoundError(f"protocol is not exist")

    @classmethod
    def register(cls,server,protocol):
        return cls(server=server,protocol = protocol)

    def __call__(self,method:str,*args):
        # todo support kwargs
        self.method = method
        self.args = args
        self._kwargs= {}

        self.is_method_valid()
        self.is_parameter_valid()

        res = getattr(self.__server,self.method)(*self.args)

        return res

    def parse(self,request_data):
        if isinstance(request_data,str):
            _data = json.loads(request_data)       

    def is_protocol_valid(self):
        protocol_keys = self.protocol.keys()
        if "methods" not in protocol_keys \
            or "server" not in protocol_keys:
            raise AttributeError(f"protocol is invalid,a least include 'method','server' fields")
        return True

    def is_method_valid(self):
        if  self.method not in self.protocol.get("methods").keys():
            print(f"{self.method} is undefined, please modify protocol")
            return False
        if self.method.startswith("__"):
            print(f"{self.method} can not start with __")
            return False
        try:
            func = getattr(self.__server,self.method)
        except AttributeError:
            print(f"{self.method} is undefined, please modify server instance")
            return False
        if not callable(func):
            print(f"{self.method} is not callable")
        return True

    def is_parameter_valid(self):
        ## 1 校验位置参数个数是否合法
        expect_paramters = self.protocol.get("methods").get(self.method).get("parameters")
        if len(self.args)!=len(expect_paramters.keys()):
            raise AttributeError(
                f"method:{self.method} expect to get {len(expect_paramters.keys())} position parameters,but got:{len(self.args)}"
            )
        ## 2 校验参数类型类型是否合法
        for index,item in enumerate(expect_paramters.items()):
            arg_name,expect_type = item
            if not isinstance(self.args[index],guess_type(expect_type)):
                raise TypeError(
                    f"param {arg_name} expect get {expect_type} type,but get {type(self.args[index])}"
                )
        return True

    def is_server_valid(self):
        ## TODO
        ...

def guess_type(type_str:str):
    if type_str.lower()=="string":
        return str
    if type_str.lower()=="int":
        return int
    if type_str.lower()=="list":
        return list
    if type_str.lower()=="dict":
        return map
    else:
        raise TypeError(f"undefined type:{type_str} only support (string,int,list,dict)")
                