# Simple RPC

- 默认端口：1840

## 传输层协议

请求协议

```text
version:1\r\n
content-length:xx\r\n
\r\n
payload:{}
```

响应协议

```text
version:1\r\n
content-length:xx\r\n
\r\n
payload:{}
```

## 应用层协议(json)
#### json protocol
```json
{
    
}

```
#### payload
##### request
```
{
    "method":[arg1,arg2,arg3]
}

```
#### response
{
    "return":any
}


## demo

### python

#### server
```python
class TestServer(BaseServer):

    def __init__(self, ip="127.0.0.1", port=9527, protocol=None) -> None:
        super().__init__(ip, port, protocol)

    def add(self,a,b):
        return a+b

    def sub(self,a,b):
        return a-b

ts = TestServer(protocol=os.path.join(os.path.dirname(__file__),"test_protocol.json"))
ts.start()

```

#### client
```python
class TestClient(BaseClient):

    def __init__(self, remote="127.0.0.1", remote_port=9527, name=None) -> None:
        super().__init__(remote, remote_port, name)



with TestClient() as tc:
    print(tc.add(1,2))
    print(tc.sub(9,1))


```

#### protocol
```json
{
    "server":"TestServer",
    "methods":{
        "add":{
            "parameters":{
                "a":"int",
                "b":"int"
            },
            "return":"int"
        },
        "sub":{
            "parameters":{
                "a":"int",
                "b":"int"
            },
            "return":"int"
        }
    }
}

```

