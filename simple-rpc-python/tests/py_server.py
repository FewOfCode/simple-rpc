import os,sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from py.server import BaseServer

class TestServer(BaseServer):

    def __init__(self, ip="127.0.0.1", port=9527, protocol=None) -> None:
        super().__init__(ip, port, protocol)

    def add(self,a,b):
        return a+b

    def sub(self,a,b):
        return a-b

if __name__ =="__main__":
    ts = TestServer(protocol=os.path.join(os.path.dirname(__file__),"test_protocol.json"))
    ts.start()