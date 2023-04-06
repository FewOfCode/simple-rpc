package main

import (
	"fmt"

	lib "github.com/FewOfCode/simple-rpc"
)

func main() {
	client, err := lib.NewClient("127.0.0.1", 8000)
	if err != nil {
		fmt.Println("dial failed, err", err)
		return
	}
	defer client.Close()
	params := map[string]interface{}{
		"param1": 2,
		"param2": 1,
	}
	options := map[string]interface{}{
		"Attr1": 11,
	}
	result, err := client.Call("Math", "Sub", params, options)
	if err != nil {
		fmt.Println("call rpa error", err)
	}
	fmt.Println(">>> get res", result.Result)
}
