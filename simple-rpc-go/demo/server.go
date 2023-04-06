package main

import (
	proto "protocol"

	lib "github.com/FewOfCode/simple-rpc"
)

func main() {
	// 注册下方法到全局MAP
	server := lib.NewServer("127.0.0.1", 8000)
	server.Register("Math", proto.Math{})
	server.Run()
}
