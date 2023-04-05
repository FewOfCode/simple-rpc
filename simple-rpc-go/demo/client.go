package main

import (
	"bytes"
	"encoding/gob"
	"fmt"
	"net"

	lib "github.com/FewOfCode/simple-rpc"
)

func main() {
	conn, err := net.Dial("tcp", "127.0.0.1:8000")
	if err != nil {
		fmt.Println("dial failed, err", err)
		return
	}
	defer conn.Close()
	d := lib.Entry{
		MethodName: "Sub",
		Parameters: map[string]interface{}{
			"param1": 2,
			"param2": 1,
		},
		MethodClass: "Math",
		Options: map[string]interface{}{
			"Attr1": 11,
		},
	}
	// msg, err := json.Marshal(d)

	var buf bytes.Buffer
	bufEnc := gob.NewEncoder(&buf)
	// 编码器对数据编码
	if err := bufEnc.Encode(d); err != nil {
		fmt.Println("encode error", err)
	} else {
		msg := buf.Bytes()
		// lib.Pack()
		_msg, err := lib.Pack(msg)
		if err != nil {
			fmt.Println("get error", err)
		}
		fmt.Println("after pack", _msg)
		conn.Write(_msg)
		// reader := bufio.NewReader(conn)

		// res:=U
	}

}
