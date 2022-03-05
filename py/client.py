
import json
import socket
import threading
import time
from py.handle import read_header,parse_header_line
from py.frame import RequestMessage
class BaseClient(object):

    def __init__(self,remote="127.0.0.1",remote_port=9527,name =None) -> None:
        self.__client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__client.connect((remote, remote_port))
    
    def __call__(self, method, *args, **kwargs):
        # todo support kwargs
        print("call method",method,args,kwargs)
        if isinstance(args,tuple):
            args = list(args)
        payload = json.dumps({method:args},ensure_ascii=False)
        msg:RequestMessage = RequestMessage.pack(message=payload)
        self.__client.sendall(msg)
        header = read_header(socket=self.__client) #
        print(f"get header :{header}")
        payload_length = header.get("content-length",None)
        if payload_length and int(payload_length)!=0:
            payload = self.__client.recv(int(payload_length)).decode("utf-8")
            print(f"get response:{payload}")  
            payload_ = json.loads(payload)
            return payload_.get("return",None)
        else:
            return None

    def __getattr__(self, method):
        return lambda *args, **kwargs: self(method, *args, **kwargs)

    def  __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.__client:
            self.__client.close()



