package src

import (
	"bytes"
	"encoding/gob"
	"fmt"
	"reflect"
)

var simpleRpcApi map[string]reflect.Value = make(map[string]reflect.Value)

func Register(name string, T interface{}) {
	if _, ok := simpleRpcApi[name]; ok {
		return
	}
	simpleRpcApi[name] = reflect.ValueOf(T)
}

type Entry struct {
	MethodName  string                 `json:"method_name"`
	Parameters  map[string]interface{} `json:"parameters"`
	MethodClass string                 `json:"method_class"`
	Options     map[string]interface{} `json:"options"`
}

type Result struct {
	Result interface{} `json:"result"`
}

func (m *Entry) Call() (interface{}, error) {
	st := simpleRpcApi[m.MethodClass]
	args := make([]reflect.Value, 0, len(m.Parameters))
	for _, arg := range m.Parameters {
		args = append(args, reflect.ValueOf(arg))
	}
	method := st.MethodByName(m.MethodName)
	fmt.Println("call class --> ", method, args)

	res := method.Call(args)

	return res, nil
}

func Handle(header map[string]string, body []byte) (interface{}, error) {
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
	return entry.Call()
}
