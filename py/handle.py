
import time
def read_header(socket):
    ## 参考http协议
    line = b""
    headers = {}
    while True:
        part = socket.recv(1)
        if part == b"":
            raise ConnectionResetError
        elif part != b"\n":
            line+=part
        elif part == b"\n":
            if  line in (b'\r\n', b'\n', b''):
                break
            else:
                headers.update(parse_header_line(line))
                line = b"" 
        # elif part == b"":
        #     raise ConnectionResetError(f">>> connection: {socket} close")
    return headers

def parse_header_line(line):
    if isinstance(line,bytes):
        line = line.decode("utf-8")
    key,value =line.split(":")
    return {key:value}