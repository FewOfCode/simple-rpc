

import time,json
class RequestMessage():

    @classmethod
    def pack(cls,message) -> bytes:
        if isinstance(message,bytes):
            message = message.decode("utf-8")
        elif isinstance(message,dict):
            message = json.dumps(message,ensure_ascii=False)
        else:
            message = message
        payload = f"""version:1\ncontent-length:{len(message)}\n\n{message}""".encode("utf-8")
        return payload


    @classmethod
    def from_socket(socket):
        ...

    def read_header(socket):
        ## 参考http协议
        line = b""
        headers = {}
        while True:
            part = socket.recv(1)
            if part != b"\n":
                line+=part
            elif part == b"\n":
                if  line in (b'\r\n', b'\n', b''):
                    break
                else:
                    headers.update(parse_header_line(line))
                    line = b""  
        return headers

    def parse_header_line(line):
        if isinstance(line,bytes):
            line = line.decode("utf-8")
        key,value =line.split(":")
        return {key:value}

class ResponseMessage():
    ...