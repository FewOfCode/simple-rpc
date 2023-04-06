package src

import (
	"bufio"
	"bytes"
	"encoding/gob"
	"fmt"
	"net"
	"reflect"
)

type Server struct {
	Addr   string
	Port   int
	ApiSet map[string]reflect.Value // api 集合
}

func NewServer(addr string, port int) *Server {
	return &Server{Addr: addr, ApiSet: make(map[string]reflect.Value), Port: port}
}

func (s *Server) Register(name string, T interface{}) {
	if _, ok := s.ApiSet[name]; ok {
		return
	}
	s.ApiSet[name] = reflect.ValueOf(T)
}

// 运行服务
func (s *Server) Run() {
	gob.Register(Result{})
	addr := fmt.Sprintf("%s:%d", s.Addr, s.Port)
	fmt.Println("begin to listen:", addr)
	listen, err := net.Listen("tcp", addr)
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
		go Process(conn, s) // 启动一个goroutine处理连接
	}
}

// 处理函数
func Process(conn net.Conn, s *Server) {
	defer conn.Close() // 关闭连接
	reader := bufio.NewReader(conn)
	for {
		header, body, err := Unpack(reader)
		if err != nil {
			fmt.Println("get message error", err)
			break
		}
		res, err := Handle(header, body, s)
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
			fmt.Println("get execute result", string(_msg))
			conn.Write(_msg)
		}
	}
}
