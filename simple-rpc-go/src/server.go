package src

import (
	"bufio"
	"bytes"
	"encoding/gob"
	"fmt"
	"net"
)

// 处理函数
func Process(conn net.Conn) {
	defer conn.Close() // 关闭连接
	reader := bufio.NewReader(conn)
	for {
		header, body, err := Unpack(reader)
		if err != nil {
			fmt.Println("get message error", err)
			break
		}
		res, err := Handle(header, body)
		if err != nil {
			fmt.Println("handle error", err)
			break
		}
		// 把结果发送出去
		fmt.Println("call method result", res)
		response := Result{
			Result: res,
		}
		var buf bytes.Buffer
		bufEnc := gob.NewEncoder(&buf)
		// 编码器对数据编码
		if err := bufEnc.Encode(response); err != nil {
			fmt.Println("encode result error", err)
		} else {
			msg := buf.Bytes()
			_msg, err := Pack(msg)
			if err != nil {
				fmt.Println("get error when pack result", err)
			}
			conn.Write(_msg)
		}
	}
}
