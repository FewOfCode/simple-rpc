from ast import arg
import json
import select, socket, sys,time
from telnetlib import KERMIT
import queue
from threading import Event
from tkinter.tix import Tree
from py.pool import create_task,RequestDealPool
import concurrent
from py.adapter import Adapter
from py.frame import RequestMessage
class BaseServer():

    def __init__(self,ip="127.0.0.1",port=1840,protocol=None) -> None:
        assert protocol is not None,"protocol can not be None"
        self.protocol=protocol
        self.__server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port =port 
        self.ip = ip
        self.stop_flag = Event()
        self.conn_manager = None
        self.adapter = None

    def start(self):
        self.stop_flag.clear()
        self.__server.setblocking(True) # 设置为非阻塞
        self.__server.bind((self.ip, self.port))
        self.__server.listen()
        self.conn_manager:ConnectionManager = ConnectionManager.register(self)
        self.conn_manager.inputs.append(self.__server)
        self.adapter:Adapter = Adapter.register(self,self.protocol)

        while self.conn_manager.inputs:
            # 调用一个内核 select 方法，返回可读/可写/异常的文件描述符列表,只有 文件状态改变，才会返回
            # 参数：1.需要检验是否为输入状态的socket列表，2 是否为可写状态的输出socket列表, 3是否为异常的socket列表
            # 返回的三个列表为对应的输入的子集
            # non-blocking/ blocking+select
            try:
                # print(">>> check socket list",self.conn_manager.inputs)
                readable, _, expection_s = select.select(
                    self.conn_manager.inputs, 
                    self.conn_manager.outputs, 
                    self.conn_manager.inputs,0.2)
                for s in readable:
                    if s is self.__server: 
                        #新连接进来
                        print(">>> a new connection")
                        connection, _ = s.accept()
                        connection.setblocking(True)
                        self.conn_manager.add_conn(connection) # 建立连接，新的SOCKET添加到inputs
                    else:
                        print("readable socket",s)
                        # 防止下次再次去select一次,在handle处理完后再添加回来
                        self.conn_manager.inputs.remove(s)
                        task = RequestDealPool.submit(create_task,s,self.conn_manager)
                        task.add_done_callback(self.handle)
                for exc_s in expection_s:
                    print("get exception socket ",exc_s)
                    self.conn_manager.remove_conn(conn=exc_s)
            except KeyboardInterrupt :
                self.conn_manager.close_all()
                break

    def handle(self,future):
        payload,socket_manager,socket = future.result()
        if payload is None and socket_manager is None and socket is None:
            ## client 断开连接
            return
        if payload is None:
            #没有携带payload数据
            socket_manager.add_input(socket)
        else:
            if isinstance(payload,bytes):
                payload  = payload.decode("utf-8")
            try:
                payload = json.loads(payload)
                for method_name,args in payload.items():
                    res = self.adapter(method_name,*args)
                    res_msg:RequestMessage =RequestMessage.pack({"return":res})
                    socket.sendall(res_msg)
            except json.JSONDecodeError:
                ## NOT JSON FORMAT,ignore
                print(">>> not a json format")
            finally:
                socket_manager.add_input(socket)

    def hello(self,name:str):
        return f"hello {name}"

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
    s.start()