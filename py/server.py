import json
import select, socket, sys,time
import socketserver
import queue
from threading import Event
from email.parser import Parser
from urllib import response
from handle import read_header,parse_header_line
from pool import create_task,RequestDealPool
import concurrent
from stub import Adapter

class SimpleServer():

    def __init__(self,ip="127.0.0.1",port=9527) -> None:
        self.__server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port =port 
        self.ip = ip
        self.stop_flag = Event()
        self.conn_manager = None
        self.adapter = None

    def start(self):
        self.stop_flag.clear()
        self.__server.setblocking(0) # 设置为非阻塞
        self.__server.bind((self.ip, self.port))
        self.__server.listen()
        self.conn_manager:ConnectionManager = ConnectionManager.register(self)
        self.conn_manager.inputs.append(self.__server)
        self.adapter:Adapter = Adapter.register(self)

        while self.conn_manager.inputs:
            # 调用一个内核 select 方法，返回可读/可写/异常的文件描述符列表
            # 参数：1.需要检验是否为输入状态的socket 列表，2 是否为可写状态的输出socket 列表, 3是否为异常的socket 列表
            # 返回的三个列表为对应的输入的子集
            # print(self.conn_manager.inputs)
            readable, _, _ = select.select(
                self.conn_manager.inputs, 
                self.conn_manager.outputs, 
                self.conn_manager.outputs)
            for s in readable:
                if s is self.__server:
                    #新连接进来
                    print(">>> a new connection")
                    connection, _ = s.accept()
                    connection.setblocking(0)
                    self.conn_manager.add_conn(connection) # 建立连接，新的SOCKET添加到inputs
                else:
                    # 防止下次再次去select一次，在handle处理完后再添加回来
                    self.conn_manager.inputs.remove(s)
                    task = RequestDealPool.submit(create_task,s,self.conn_manager)
                    task.add_done_callback(self.handle)

    def handle(self,future:concurrent.futures.Future):
        payload,socket_manager,socket = future.result()
        if payload is None and socket_manager is None and socket is None:
            return
        if payload is None:
            socket_manager.add_input(socket)
        else:
            if isinstance(payload,bytes):
                payload  = payload.decode("utf-8")
            try:
                payload = json.loads(payload)
                response = f"this is simpleRPC,i get request:{payload}"
                msg = f"""version:1\ncontent-length:{len(response)}\n\n{response}"""
                print("send response",msg)
                socket.sendall(msg.encode("utf-8")) #
            except:
                ## NOT JSON FORMAT,ignore
                print(">>> not a json format")
            finally:
                socket_manager.add_input(socket)


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

if  __name__=="__main__":
    # import simple

    s = SimpleServer()
    s.start()