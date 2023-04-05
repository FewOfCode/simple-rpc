package src

import (
	"bufio"
	"bytes"
	"encoding/binary"
	"fmt"
	"io"
	"strconv"
	"strings"
)

func Pack(body []byte) ([]byte, error) {
	// 读取消息的长度，转换成int32类型（占4个字节）
	var length = len(body)
	var pkg = new(bytes.Buffer)
	// 先写入头部
	header := []byte(fmt.Sprintf("version:1\r\ncontent-length:%d\r\n\r\n", length))
	err := binary.Write(pkg, binary.LittleEndian, header)
	if err != nil {
		return nil, err
	}

	// 写入消息实体
	err = binary.Write(pkg, binary.LittleEndian, body)
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

// 编码
// func encode(data interface) ([]byte, error) {
// 	//得到字节数组的编码器
// 	var buf bytes.Buffer
// 	bufEnc := gob.NewEncoder(&buf)
// 	// 编码器对数据编码
// 	if err := bufEnc.Encode(data); err != nil {
// 		return nil, err
// 	}
// 	return buf.Bytes(), nil
// }

// // 解码
// func decode(b []byte) (RPCData, error) {
// 	buf := bytes.NewBuffer(b)
// 	// 得到字节数组解码器
// 	bufDec := gob.NewDecoder(buf)
// 	// 解码器对数据节码
// 	var data RPCData
// 	if err := bufDec.Decode(&data); err != nil {
// 		return data, err
// 	}
// 	return data, nil
// }
