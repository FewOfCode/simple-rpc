import os,sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from py.client import BaseClient


class TestClient(BaseClient):

    def __init__(self, remote="127.0.0.1", remote_port=1840, name=None) -> None:
        super().__init__(remote, remote_port, name)


if __name__ =="__main__":
    with TestClient() as tc:
        print(tc.add(1,2))
        # print(tc.sub(9,1))
    # import time
    # time.sleep(5)