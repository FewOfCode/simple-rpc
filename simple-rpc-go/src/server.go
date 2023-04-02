package main

import (
	"bufio"
	"encoding/json"
	"fmt"
	"net"
)

// 处理函数
func process(conn net.Conn) {
	defer conn.Close() // 关闭连接
	reader := bufio.NewReader(conn)
	for {
		header, body, err := Unpack(reader)
		if err != nil {
			fmt.Println("get message error", err)
		}
		result, err := handle(header, body)
		if err != nil {
			fmt.Println("handle error", err)
		}
		// 把结果发送出去
		var msg = make(map[string]interface{})
		msg["return"] = result
		b, err := json.Marshal(msg)
		if err != nil {
			fmt.Println("convert to  json string error", err)
		}
		conn.Write(b)
	}
}

// func main() {
// 	listen, err := net.Listen("tcp", "127.0.0.1:8000")
// 	if err != nil {
// 		fmt.Println("listen failed, err:", err)
// 		return
// 	}
// 	for {
// 		conn, err := listen.Accept() // 建立连接
// 		if err != nil {
// 			fmt.Println("accept failed, err:", err)
// 			continue
// 		}
// 		go process(conn) // 启动一个goroutine处理连接
// 	}
// }
