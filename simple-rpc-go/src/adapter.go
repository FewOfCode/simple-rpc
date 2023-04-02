package main

import (
	"encoding/json"
	"fmt"
	"reflect"
)

var simpleRpcApi map[string]interface{}

func register(simpleRpcApi interface{}) {
	// if simpleRpcApi != nil {

	// } else {
	// 	simpleRpcApi := make(map[string]interface{})
	// }

}

// func

type Method struct {
	MethodName  string                 `json:"method_name"`
	Parameters  map[string]interface{} `json:"parameters"`
	MethodClass string                 `json:"method_class"`
	Options     map[string]interface{} `json:"options"`
}

//NewPerson 构造函数
func NewMethod(methodName, methodClass string, parameters, options map[string]interface{}) *Method {
	return &Method{
		MethodName:  methodName,
		Parameters:  parameters,
		MethodClass: methodClass,
		Options:     options,
	}
}

func (m *Method) call() (interface{}, error) {
	ref := reflect.ValueOf(&simpleRpcApi)

	f := reflect.ValueOf(ref).MethodByName(m.MethodName)

	args := make([]reflect.Value, 0, len(m.Parameters))

	for _, arg := range m.Parameters {
		args = append(args, reflect.ValueOf(arg))
	}
	fmt.Println("call method --> ", f, args)
	results := f.Call(args)
	fmt.Println(results, ">>>>>")

	return nil, nil
}

func handle(header map[string]string, body string) (interface{}, error) {
	fmt.Println("get message ", header, body)
	var method Method
	err := json.Unmarshal([]byte(body), &method)
	if err != nil {
		fmt.Println("convert str to json error", err)
		return nil, err
	}
	return method.call()
}
