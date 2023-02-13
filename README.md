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
  "method_name": "string",
  "parameters": {
    "params1": "string",
    "params2": 0,
    "params3": {},
    "params4": []
  },
  "options": {
    "java_interface_name": "string"
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
  "engine": "SimpleRPC",
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
  "server": "TestServer",
  "methods": {
    "add": {
      "parameters": {
        "a": "int",
        "b": "int"
      },
      "return": "int"
    },
    "sub": {
      "parameters": {
        "a": "int",
        "b": "int"
      },
      "return": "int"
    }
  }
}

```

# 开发计划

当前版本：v1.0.x

> 大版本：用于里程碑式更新
>
> 中版本：用于功能更新或重大bug修复
>
> 小版本：用于小功能更新或bug修复


v1.0.x 完成以下目标：

- 规范传输层协议和应用层协议
- 开发实现simple-rpc基本功能：根据协议实现基本的远程过程调用(Python、JavaScript、Java)，能够实现各个开发语言自己调用自己
- 测试各个开发语言之间相互调用
- Demo和使用文档(Python、JavaScript、Java)

v1.1.x 完成以下目标：

> 规划中...

- 根据协议生成代码
- 服务发现：客户端怎么找到能够调用rpc的服务器的ip和端口。注册中心：zookeeper/nacos