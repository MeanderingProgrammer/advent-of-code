package main

import(
    "fmt"
    "io/ioutil"
    "strconv"
    "strings"
)

func main() {
    content := getContent()

    fmt.Printf("Part 1 = %d \n", windowIncreases(content, 1))
    fmt.Printf("Part 2 = %d \n", windowIncreases(content, 3))
}

func getContent() []string {
    content, _ := ioutil.ReadFile("data.txt")
    return strings.Split(string(content), "\r\n")
}

func windowIncreases(content []string, windowSize int) int {
    increases := 0

    slidingContent := content[1:]
    for i := range slidingContent[:len(slidingContent) - windowSize + 1] {
        v1 := sum(content[i:i+windowSize])
        v2 := sum(slidingContent[i:i+windowSize])
        if (v2 > v1) {
            increases++
        }
    }

    return increases
}

func sum(values []string) int {
    result := 0
    for _, value := range values {
        v, _ := strconv.Atoi(value)
        result += v
    }
    return result
}
