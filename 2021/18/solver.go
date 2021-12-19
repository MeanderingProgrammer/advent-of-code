package main

import(
    "fmt"
    "io/ioutil"
    "strconv"
    "strings"
)

type Element struct {
    regular int
    nested SnailNumber
}

func (element Element) toString() string {
    emptyNested := SnailNumber{}
    if element.nested != emptyNested {
        return element.nested.toString()
    } else {
        return strconv.FormatInt(int64(element.regular), 10)
    }
}

type SnailNumber struct {
    left *Element
    right *Element
}

func (snailNumber SnailNumber) toString() string {
    var result strings.Builder
    result.WriteString("[")
    result.WriteString(snailNumber.left.toString())
    result.WriteString(",")
    result.WriteString(snailNumber.right.toString())
    result.WriteString("]")
    return result.String()
}

func (v1 SnailNumber) add(v2 SnailNumber) SnailNumber {
    return SnailNumber{
        left: &Element{nested: v1},
        right: &Element{nested: v2},
    }
}

func main() {
    numbers := getData()

    sum := numbers[0]
    fmt.Println(sum.toString())
    for _, value := range numbers[1:] {
        fmt.Println(value.toString())
        sum = sum.add(value)
    }
    fmt.Println(sum.toString())
}

func getData() []SnailNumber {
    data, _ := ioutil.ReadFile("sample.txt")
    rawNumbers := strings.Split(string(data), "\r\n")
    var result []SnailNumber
    for _, rawNumber := range rawNumbers {
        snailNumber := parseSnailNumber(rawNumber)
        result = append(result, snailNumber)
    }
    return result
}

func parseSnailNumber(rawNumber string) SnailNumber {
    unnested := rawNumber[1:len(rawNumber) - 1]
    split := getSplit(unnested)
    left, right := unnested[:split], unnested[split + 1:]
    return SnailNumber{
        left: parseElement(left), 
        right: parseElement(right),
    }
}

func getSplit(unnested string) int {
    level := 0
    for i, char := range unnested {
        if char == ',' && level == 0 {
            return i
        } else if char == '[' {
            level++
        } else if char == ']' {
            level--
        }
    }
    return -1
}

func parseElement(element string) *Element {
    result := Element{}
    if element[0] == '[' {
        result.nested = parseSnailNumber(element)
    } else {
        value, _ := strconv.Atoi(element)
        result.regular = value
    }
    return &result
}
