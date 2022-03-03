## todo deal every request in threadPool
import concurrent.futures
import os
from handle import read_header,parse_header_line
# 网络IO处理线程池
RequestDealPool = concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count()*3)

def create_task(socket,socket_manager):
    # print(socket)
    try:
        header = read_header(socket=socket) #
    except ConnectionResetError as exc:
        print(">>> client close connection")
        socket_manager.remove_conn(socket)
        return None,None,None
    print(f"get header :{header}")
    payload_length = header.get("content-length",None)
    if payload_length  and int(payload_length)!=0:
        payload = socket.recv(int(payload_length)).decode("utf-8")
        print(f"get payload:{payload}")
    else:
        payload = None
    return payload,socket_manager,socket

