from asyncio.streams import StreamReader   

def read_header(socket):
    ## 参考http协议
    ## @https://stackoverflow.com/questions/667640/how-to-tell-if-a-connection-is-dead-in-python
    line = b""
    headers = {}
    disconnect_check_count = 0 # 用来判断是否断开，当收到三次空的byte的时候，判断客户端已经断开
    while True:
        part = socket.recv(1)
        if len(part) == 0:
            disconnect_check_count+=1
            ## 客户端断开后会发送空的字符串 b""
            ## @https://www.rhumbarlv.com/how-do-you-make-a-socket-recv-non-blocking/#:~:text=In%20blocking%20mode%2C%20the%20recv%2C%20send%2C%20connect%20%28TCP,until%20the%20socket%20is%20ready.%20Is%20connect%20blocking%3F
            if disconnect_check_count > 3:
                raise ConnectionResetError
        else:
            if part != b"\n":
                line+=part
            else:
                if  line in (b'\r\n', b'\n',b''):
                    break
                else:
                    headers.update(parse_header_line(line))
                    line = b"" 
    return headers


async def async_read_header(stream_reader:StreamReader):
    line = b""
    headers = {}
    disconnect_check_count=0 # 用来判断是否断开，当收到三次空的byte的时候，判断客户端已经断开
    while True:
        line = await stream_reader.readline()
        if len(line) == 0:
            disconnect_check_count+=1
            ## 客户端断开后会发送空的字符串 b""
            ## @https://www.rhumbarlv.com/how-do-you-make-a-socket-recv-non-blocking/#:~:text=In%20blocking%20mode%2C%20the%20recv%2C%20send%2C%20connect%20%28TCP,until%20the%20socket%20is%20ready.%20Is%20connect%20blocking%3F
            if disconnect_check_count > 3:
                raise ConnectionResetError
        else:
            if  line in (b'\r\n', b'\n',b''): # 请求头和请求body之间有一个分割行 
                break
            else:
                headers.update(parse_header_line(line))
                line = b""     
    return headers

def parse_header_line(line):
    if isinstance(line,bytes):
        line = line.decode("utf-8")
    print(line)
    key,value =line.split(":")
    return {key:value}