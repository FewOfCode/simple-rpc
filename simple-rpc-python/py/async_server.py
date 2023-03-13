import os,sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import queue
from threading import Event
from py.adapter import Adapter
import asyncio
from asyncio.streams import StreamReader,StreamWriter
from py.handle import read_header

class BaseServer():

    def __init__(self,ip="127.0.0.1",port=1840,protocol=None) -> None:
        # assert protocol is not None,"protocol can not be None"
        self.protocol=protocol
        self.port =port 
        self.ip = ip
        self.stop_flag = Event()
        self.conn_manager = None
        self.adapter = None
        self.__server=None

    async def start(self):
        try:
            self.stop_flag.clear()
            self.conn_manager:ConnectionManager = ConnectionManager.register(self)
            self.__server = await asyncio.start_server(client_connected_cb, self.ip, self.port)
            async with self.__server:
                await self.__server.serve_forever()
            self.conn_manager.inputs.append(self.__server)
            self.adapter:Adapter = Adapter.register(self,self.protocol)
        except KeyboardInterrupt:
            #TODO close socket and eventloop
            print(">>> server close")

    ## TODO SUPPORT ASYNC FUNCTION
    def add(self,a,b):
        return a+b

    def sub(self,a,b):
        return a-b


async def client_connected_cb(reader:StreamReader, writer:StreamWriter):
    # todo add transport to conn manager
    while True: # todo break
        try:
            header = await read_header(reader)
        except ConnectionResetError as exc:
            print(">>> conn reset when read header") # todo remove conn fron manager
        print(f"get header :{header}")
        payload_length = header.get("content-length",None)
        if payload_length  and int(payload_length)!=0:
            payload = await reader.read(payload_length)
            print(f"get payload:{payload}")
        else:
            payload = None

class ConnectionManager():
    
    __instance = None

    def __new__(cls,*args,**kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance          

    def __init__(self,server) -> None:
        self.__server = server
        self.conn_cache={}
        self.msg_cache= {}
        self.inputs,self.outputs,self.exceptions=[],[],[]
    
    @classmethod
    def register(cls,server)->"ConnectionManager":
        return cls(server=server)

    def add_conn(self,conn):
        if conn not in self.inputs:
            self.inputs.append(conn)
        if conn not in self.conn_cache.keys():
            self.conn_cache.update({conn.fileno():conn})
            self.msg_cache.update({conn.fileno():queue.Queue()})
    
    def add_input(self,conn):
        if conn not in self.inputs:
            self.inputs.append(conn)   
    
    def add_output(self,conn):
        if conn not in self.outputs:
            self.outputs.append(conn)

    def remove_conn(self,conn):
        if conn in self.inputs:
            self.inputs.remove(conn)  
        if conn in self.outputs:
            self.outputs.remove(conn)
        if conn in self.exceptions:
            self.exceptions.remove(conn)

    def close_all(self):
        for s in self.inputs:
            s.close()
        for s in self.outputs:
            self.close()
        for s in self.exceptions:
            s.close()

if  __name__=="__main__":
    # import simple
    s = BaseServer()
    asyncio.run(s.start())