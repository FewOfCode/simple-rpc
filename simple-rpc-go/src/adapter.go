package src

import (
	"bytes"
	"encoding/gob"
	"fmt"
	"reflect"
)

type Entry struct {
	MethodName string                 `json:"method_name"`
	Parameters map[string]interface{} `json:"parameters"`
	ClassName  string                 `json:"class_class"`
	Options    map[string]interface{} `json:"options"`
}

type Result struct {
	Result []interface{} `json:"result"`
}

func (m *Entry) Call(s *Server) ([]interface{}, error) {
	st := s.ApiSet[m.ClassName]
	args := make([]reflect.Value, 0, len(m.Parameters))
	for _, arg := range m.Parameters {
		args = append(args, reflect.ValueOf(arg))
	}
	method := st.MethodByName(m.MethodName)
	fmt.Println("call class --> ", method, args)

	out := method.Call(args)
	outArgs := make([]interface{}, 0, len(out))
	for _, o := range out {
		outArgs = append(outArgs, o.Interface())
	}
	return outArgs, nil
}

func Handle(header map[string]string, body []byte, s *Server) ([]interface{}, error) {
	var entry Entry
	// err := json.Unmarshal(body, &entry)
	buf := bytes.NewBuffer(body)
	// 得到字节数组解码器
	bufDec := gob.NewDecoder(buf)
	err := bufDec.Decode(&entry)
	fmt.Println("decode data", entry, reflect.TypeOf(entry.Options["Attr1"]))
	if err != nil {
		fmt.Println("convert str to json error", err)
		return nil, err
	}
	return entry.Call(s)
}
