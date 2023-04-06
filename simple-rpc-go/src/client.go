package src

import (
	"bufio"
	"bytes"
	"encoding/gob"
	"fmt"
	"net"
)

type Client struct {
	Addr string
	Port int
	Conn net.Conn
}

func NewClient(Addr string, Port int) (*Client, error) {
	addr := fmt.Sprintf("%s:%d", Addr, Port)
	conn, err := net.Dial("tcp", addr)
	if err != nil {
		fmt.Println("dial failed, err", err)
		return nil, err
	}
	return &Client{Addr: Addr, Port: Port, Conn: conn}, nil
}

func (c *Client) Close() {
	c.Conn.Close()
}

func (c *Client) Call(ClassName string, MethodName string, Parameters map[string]interface{}, Options map[string]interface{}) (*Result, error) {
	d := Entry{
		MethodName: MethodName,
		Parameters: Parameters,
		ClassName:  ClassName,
		Options:    Options,
	}
	// msg, err := json.Marshal(d)

	var buf bytes.Buffer
	bufEnc := gob.NewEncoder(&buf)
	// 编码器对数据编码
	if err := bufEnc.Encode(d); err != nil {
		fmt.Println("encode error", err)
		return nil, err
	} else {
		msg := buf.Bytes()
		_msg, err := Pack(msg)
		if err != nil {
			fmt.Println("get error", err)
		}
		fmt.Println("after pack", _msg)
		c.Conn.Write(_msg)
		// await return call result
		reader := bufio.NewReader(c.Conn)
		_, body, err := Unpack(reader)
		if err != nil {
			fmt.Println("get response  error", err)
			return nil, err
		} else {
			buf := bytes.NewBuffer(body)
			var res Result
			// 得到字节数组解码器
			bufDec := gob.NewDecoder(buf)
			err := bufDec.Decode(&res)
			if err != nil {
				fmt.Println("decode result error", err)
				return nil, err
			}
			return &res, nil
		}
	}
}
