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
  "class_name":"class_name",
  "class_params":{}, // 对应的类的类参数处理
  "parameters": {
    "params1": ["aaa","string"],
    "params2": [0,"int"],
    "params3": [{}],
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
	"engine":"simpleRpc",
  "version": "v1",
  "services": {
    "{{service1}}": {
      "meta": {
      },
      "types": {
        "{{自定义参数类型名称1}}": "{{自定义参数结构}}"
      },
      "methods": {
        "{{类名}}": {
          "{{方法名}}": {
            "parameters": {
              "参数一": "int",
              "参数二": "{{自定义参数类型名称1}}"
            },
            "return": "int"
          }
        },
        "{{类名2}}": {
          "{{方法名}}": {
            "parameters": {
              "参数一": "int",
              "参数二": "{{自定义参数类型名称1}}"
            },
            "return": "int"
          }
        }
      },
      "options": {
        "ConnectTimeout": 1000,
        "SSL": false
      }
    },
    "{{service2}}": {}
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

#### python
- [server](/simple-rpc-python/demo/py_server.py)
- [async_server](/simple-rpc-python/demo/async_py_server.py)
- [client](/simple-rpc-python/demo/py_client.py)


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