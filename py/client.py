import json
import socket
import threading
import time
from handle import read_header,parse_header_line
    # while True:
    #     try:
    #         data = s.recv(1024)
    #         print('Received', repr(data))
    #         s.send("close".encode("utf-8"))
    #     except:
    #         break
    #     time.sleep(1)


if __name__ =="__main__":
    HOST = '127.0.0.1'    # The remote host
    PORT = 9527              # The same port as used by the server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        payload = json.dumps({"hello":["linlin"]},ensure_ascii=False)
        msg = f"""version:1\ncontent-length:{len(payload)}\n\n{payload}"""
        s.sendall(msg.encode("utf-8"))
        header = read_header(socket=s) #
        print(f"get header :{header}")
        payload_length = header.get("content-length",None)
        if payload_length  and int(payload_length)!=0:
            payload = s.recv(int(payload_length)).decode("utf-8")
            print(f"get response:{payload}")
