# 一个简单的RPC尝试
## 传输层协议
```text
request:
    version:1<space>\r\n
    content-length:xx<space>\r\n
    \r\n
    .......  payload

```

```text
response:
    version:1<space>\r\n
    content-length:xx<space>\r\n
    \r\n
    .......  payload    


```
## 应用层协议(json)
#### json protocol
```json
{
    
}

```
#### payload
```
{
    "method":[arg1,arg2,arg3]
}

```