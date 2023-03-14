import queue
from threading import Event
from py.adapter import Adapter
import asyncio
from asyncio.streams import StreamReader,StreamWriter
from py.handle import async_read_header
import json
from py.adapter import Adapter
from functools import partial
from py.frame import RequestMessage
import signal,socket

def loop_wake_up(loop):
    loop.call_later(0.1,loop_wake_up,loop)



class AsyncBaseServer():
    def __init__(self,ip="127.0.0.1",port=1840,protocol=None) -> None:
        assert protocol is not None,"protocol can not be None"
        self.protocol=protocol
        self.port =port 
        self.ip = ip
        self.adapter:Adapter = Adapter.register(self,self.protocol)
        self.__server=None

    async def start(self):
        # add loop wake up task,then can interrupt server by ctrl + c
        loop = asyncio.get_event_loop()
        loop.call_later(0.1,loop_wake_up,loop)
        try:
            self.__server = await asyncio.start_server(partial(client_connected_cb,server=self), self.ip, self.port)
            async with self.__server:
                await self.__server.serve_forever()
        except Exception:
            self.__server.close()
            raise

    def _close(self):
        print("close server")
        self.__server.close()

    ## TODO SUPPORT ASYNC FUNCTION



async def client_connected_cb(reader:StreamReader, writer:StreamWriter,server:AsyncBaseServer=None):
    while True:
        try:
            header = await async_read_header(reader)
        except ConnectionResetError as exc:
            print(f"client close... transport:{reader._transport}")
            reader._transport.close()
            break
        print(f"get header :{header}")

        payload_length = header.get("content-length",None)
        if payload_length  and int(payload_length)!=0:
            payload = await reader.read(int(payload_length))
            print(f"get payload:{payload}")
            if isinstance(payload,bytes):
                payload  = payload.decode("utf-8")
            try:
                payload = json.loads(payload)
                for method_name,args in payload.items():
                    ##  call function and get result
                    res = server.adapter(method_name,*args)
                    res_msg:RequestMessage =RequestMessage.pack({"return":res})
                    ## write response
                    writer.write(res_msg)
                    await writer.drain()
            except json.JSONDecodeError:
                ## NOT JSON FORMAT,ignore
                print(">>> not a json format",payload)
        else:
            payload = None
        header.clear()

