package protocol

import (
	"fmt"
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
