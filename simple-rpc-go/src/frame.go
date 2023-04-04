package main

import (
	"bufio"
	"bytes"
	"encoding/binary"
	"fmt"
	"io"
	"strconv"
	"strings"
)

func Pack(body string) ([]byte, error) {
	// 读取消息的长度，转换成int32类型（占4个字节）
	var length = int32(len(body))
	var pkg = new(bytes.Buffer)
	// 先写入头部
	header := []byte(fmt.Sprintf("version:1\r\ncontent-length:%s\r\n\r\n", string(length)))
	err := binary.Write(pkg, binary.LittleEndian, header)
	if err != nil {
		return nil, err
	}

	// 写入消息实体
	err = binary.Write(pkg, binary.LittleEndian, []byte(body))
	if err != nil {
		return nil, err
	}
	return pkg.Bytes(), nil
}

func Unpack(reader *bufio.Reader) (map[string]string, []byte, error) {
	// 读取消息的
	header := make(map[string]string)

	//先读取header
	for {
		line, _, err := reader.ReadLine()
		if err == io.EOF {
			break
		}
		if err != nil {
			fmt.Println("read from client failed, err:", err)
			return nil, nil, err
		}
		if len(line) == 0 {
			fmt.Println(">>> get header finish,header :", header)
			break
		}
		//分割请求头
		slice := strings.Split(string(line), ":")
		if len(slice) != 0 {
			header[slice[0]] = slice[1]
		}
	}
	// 读取body
	content_length, err := strconv.ParseInt(header["content-length"], 10, 32)
	if err != nil {
		fmt.Println("convert content-length error", err)
		return nil, nil, err
	}
	body := make([]byte, content_length)
	_, err = reader.Read(body)
	if err != nil {
		fmt.Println("read body error", err)
		return nil, nil, err
	}
	return header, body, nil
}
