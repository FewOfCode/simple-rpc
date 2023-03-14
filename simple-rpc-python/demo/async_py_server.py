import os,sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import asyncio
from py.async_server import AsyncBaseServer

class TestServer(AsyncBaseServer):

    def __init__(self, ip="127.0.0.1", port=1840, protocol=None) -> None:
        super().__init__(ip, port, protocol)

    def add(self,a,b):
        return a+b

    def sub(self,a,b):
        return a-b

if __name__ =="__main__":
    ts = TestServer(protocol=os.path.join(os.path.dirname(__file__),"test_protocol.json"))
    loop= asyncio.get_event_loop()
    try:
        loop.run_until_complete(ts.start())
    except:
        print("close loop")
        loop.stop()
        loop.close()