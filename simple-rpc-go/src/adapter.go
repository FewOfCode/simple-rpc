package main

import (
	"encoding/json"
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

// func

type Entry struct {
	MethodName  string                 `json:"method_name"`
	Parameters  map[string]interface{} `json:"parameters"`
	MethodClass string                 `json:"method_class"`
	Options     map[string]interface{} `json:"options"`
}

func (m *Entry) Call() (interface{}, error) {
	st := simpleRpcApi[m.MethodClass]
	args := make([]reflect.Value, 0, len(m.Parameters))
	for _, arg := range m.Parameters {
		args = append(args, reflect.ValueOf(arg))
	}
	fmt.Println("call class --> ", st)

	// class := f(m.Options)
	// fmt.Println("call class --> ", class)

	// method := reflect.ValueOf(class).MethodByName(m.MethodName)
	// method.Call(args)
	// v, ok := m.Options
	// if ok {
	// 	class := f(v)
	// 	fmt.Println("call class --> ", class)
	// 	fmt.Println("call method --> ", method)
	// 	return nil, nil
	// } else {
	// 	fmt.Println("initParams format invalid")
	return nil, nil
	// }
}

func handle(header map[string]string, body []byte) (interface{}, error) {
	var entry Entry
	err := json.Unmarshal(body, &entry)
	fmt.Println("decode data", entry, reflect.TypeOf(entry.Options["Attr1"]))
	if err != nil {
		fmt.Println("convert str to json error", err)
		return nil, err
	}
	return entry.Call()
}
