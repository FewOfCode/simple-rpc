# Simple RPC

- 默认端口：1840



## 传输层协议

### 请求协议

| 字段           | 说明         | 备注 |
| -------------- | ------------ | ---- |
| version        | 传输协议版本 |      |
| content-length | payload长度  |      |
| payload        | 请求消息负载 |      |

```text
version:1\r\n
content-length:1024\r\n
\r\n
payload:xxxx
```

#### 请求协议payload规范

```json
{
  "method_name": {
    "params1": "string",
    "params2": 0,
    "params3": {},
    "params4": []
  }
}
```

### 响应协议

| 字段           | 说明         | 备注 |
| -------------- | ------------ | ---- |
| version        | 传输协议版本 |      |
| content-length | payload长度  |      |
| payload        | 响应消息负载 |      |

```text
version:1\r\n
content-length:1024\r\n
\r\n
payload:xxxx
```

#### 响应协议payload规范

```json
{
  "return": "string|number|{}|[]"
}
```



## 应用层协议定义(Json/Yaml)

### Json protocol
```json
{
  "engine":"SimpleRPC", 
  "version": "v1", 
  "methods": {
    "hello": {
      "parameters": {
        "name": "${数据类型}"
      }, 
      "return": "${数据类型}"
    }
  }
}
```
### yaml protocol

```yaml
engine: SimpleRPC
version: v1
methods:
  - hello:
      parameters: 
        name: "${数据类型}"
      return: "${数据类型}"  
```

### 数据类型定义

| 数据类型 | 说明                     |
| -------- | ------------------------ |
| string   | 普通字符串 \| 时间字符串 |
| number   | 数值                     |
| array    | 数组                     |
| object   | 对象                     |




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

