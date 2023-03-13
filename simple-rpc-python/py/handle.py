from asyncio.streams import StreamReader   


def read_header(socket):
    ## 参考http协议
    ## @https://stackoverflow.com/questions/667640/how-to-tell-if-a-connection-is-dead-in-python
    line = b""
    headers = {}
    count = 0
    while True:
        part = socket.recv(1)
        count+=1
        if len(part) == 0:
            ## 客户端断开后会发送空的字符串 b""
            ## @https://www.rhumbarlv.com/how-do-you-make-a-socket-recv-non-blocking/#:~:text=In%20blocking%20mode%2C%20the%20recv%2C%20send%2C%20connect%20%28TCP,until%20the%20socket%20is%20ready.%20Is%20connect%20blocking%3F
            raise ConnectionResetError
        else:
            if part != b"\n":
                line+=part
            else:
                if  line in (b'\r\n', b'\n', b''):
                    break
                else:
                    headers.update(parse_header_line(line))
                    line = b"" 
    return headers




async def read_header(stream_reader:StreamReader):
    line = b""
    headers = {}
    while True:
        line = await stream_reader.readline()
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