package main

import (
	"fmt"
	"reflect"
)

// 定义结构体
type User struct {
	Id   int
	Name string
	Age  int
}

// 绑方法
func (u User) Hello(arg int) int {
	fmt.Println("Hello")
	return 1
}

// 绑方法
func (u User) Add() {
	fmt.Println("Hello")
}

// 传入interface{}
func Poni(o interface{}) {
	var u User = User{1, "zs", 20}
	t := reflect.TypeOf(u)
	fmt.Println("类型：", t)
	fmt.Println("字符串类型：", t.Name())
	// 获取值
	v := reflect.ValueOf(o)
	fmt.Println(v)
	// 可以获取所有属性
	// 获取结构体字段个数：t.NumField()
	for i := 0; i < t.NumField(); i++ {
		// 取每个字段
		f := t.Field(i)
		fmt.Printf("%s : %v", f.Name, f.Type)
		// 获取字段的值信息
		// Interface()：获取字段对应的值
		val := v.Field(i).Interface()
		fmt.Println("val :", val)
	}
	fmt.Println("=================方法====================")
	for i := 0; i < t.NumMethod(); i++ {
		m := t.Method(i)
		fmt.Println(m.Name)
		fmt.Println(m.Type)
	}

}

func main() {
	u := User{1, "zs", 20}
	Poni(u)
}
