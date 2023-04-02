package main

import (
	"bytes"
	"encoding/binary"
	"encoding/json"
	"fmt"
	"net"
)

func Pack(body []byte) ([]byte, error) {
	// 读取消息的长度，转换成int32类型（占4个字节）
	var length = len(body)
	var pkg = new(bytes.Buffer)
	// 先写入头部
	header := []byte(fmt.Sprintf("version:1\r\ncontent-length:%d\r\n\r\n", length))
	err := binary.Write(pkg, binary.LittleEndian, header)
	if err != nil {
		return nil, err
	}

	// 写入消息实体
	err = binary.Write(pkg, binary.LittleEndian, body)
	if err != nil {
		return nil, err
	}
	return pkg.Bytes(), nil
}

type Method struct {
	MethodName  string                 `json:"method_name"`
	Parameters  map[string]interface{} `json:"parameters"`
	MethodClass string                 `json:"method_class"`
	Options     map[string]interface{} `json:"options"`
}

func main() {
	conn, err := net.Dial("tcp", "127.0.0.1:8000")
	if err != nil {
		fmt.Println("dial failed, err", err)
		return
	}
	defer conn.Close()
	d := Method{
		MethodName: "sub",
		Parameters: map[string]interface{}{
			"param1": 2,
			"param2": 1,
		},
		MethodClass: "Math",
		Options: map[string]interface{}{
			"timeout": 60,
		},
	}
	msg, err := json.Marshal(d)

	_msg, err := Pack(msg)
	if err != nil {
		fmt.Println("get error", err)
	}
	fmt.Println("after pack", string(_msg))
	conn.Write(_msg)
}
