package main

import(
    "fmt"
    "io/ioutil"
    "strings"
)

func main() {
    data := getData()
    fmt.Println(data)
}

func getData() []string {
    data, _ := ioutil.ReadFile("data.txt")
    return strings.Split(string(data), "\r\n")
}
