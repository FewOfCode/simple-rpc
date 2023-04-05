package main

import (
	"fmt"
	"net"

	lib "github.com/FewOfCode/simple-rpc"
)

// 供客户端调用的接口,后期支持根据协议自动生成

type SimpleRpcApi interface {
	// 所有的接口全部属于 SimpleRpcApi ，SimpleRpcApi为固定
	Sub(int, int) int
	Add(int, int) int
}

type Math struct {
	Attr1 int
}

func (t Math) Sub(arg1 int, arg2 int) int {
	fmt.Println("api is called", arg1, arg2)
	res := arg1 - arg2
	return res
}

func (t Math) Add(arg1 int, arg2 int) int {
	fmt.Println("api is called", arg1, arg2)
	res := arg1 + arg2
	return res
}

func main() {
	// 注册下方法到全局MAP
	lib.Register("Math", Math{})
	listen, err := net.Listen("tcp", "127.0.0.1:8000")
	if err != nil {
		fmt.Println("listen failed, err:", err)
		return
	}
	for {
		conn, err := listen.Accept() // 建立连接
		if err != nil {
			fmt.Println("accept failed, err:", err)
			continue
		}
		go lib.Process(conn) // 启动一个goroutine处理连接
	}
}
