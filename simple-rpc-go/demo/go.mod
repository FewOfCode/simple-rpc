module demo

go 1.17



require "github.com/FewOfCode/simple-rpc" v0.0.0
replace "github.com/FewOfCode/simple-rpc" => "../src"
require "protocol" v0.0.0
replace "protocol" => "../protocol"