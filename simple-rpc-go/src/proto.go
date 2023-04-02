package main

import (
	"fmt"
	"reflect"
)

// 供客户端调用的接口,后期支持根据协议自动生成

// type SimpleRpcApi interface {
// 	// 所有的接口全部属于 SimpleRpcApi ，SimpleRpcApi为固定
// 	sub(int, int) int
// 	add(int, int) int
// }

type Math struct {
}

func (t *Math) sub(arg1 int, arg2 int) int {
	fmt.Println("api is called", arg1, arg2)
	res := arg1 - arg2
	return res
}

func (t *Math) add(arg1 int, arg2 int) int {
	fmt.Println("api is called", arg1, arg2)
	res := arg1 + arg2
	return res
}

func main() {
	// 获取接口Person的类型对象
	var math Math = Math{}
	typeOfPerson := reflect.TypeOf(&math)
	// 打印Person的方法类型和名称
	for i := 0; i < typeOfPerson.NumMethod(); i++ {
		fmt.Printf("method is %s, type is %s, kind is %s.\n", typeOfPerson.Method(i).Name, typeOfPerson.Method(i).Type, typeOfPerson.Method(i).Type.Kind())
	}
	// method, _ := typeOfPerson.MethodByName("Run")
	// fmt.Printf("method is %s, type is %s, kind is %s.\n", method.Name, method.Type, method.Type.Kind())

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
}
