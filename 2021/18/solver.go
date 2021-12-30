package main

import(
    "fmt"
    "io/ioutil"
    "strconv"
    "strings"
)

type SnailNumber struct {
    value int
    parent *SnailNumber
    left *SnailNumber
    right *SnailNumber
}

func (snailNumber *SnailNumber) isRoot() bool {
    return snailNumber.parent == nil
}

func (snailNumber *SnailNumber) isLeaf() bool {
    return snailNumber.left == nil && snailNumber.right == nil
}

func (snailNumber *SnailNumber) toString() string {
    if snailNumber.isLeaf() {
        return strconv.FormatInt(int64(snailNumber.value), 10)
    } else {
        var result strings.Builder
        result.WriteString("[")
        result.WriteString(snailNumber.left.toString())
        result.WriteString(",")
        result.WriteString(snailNumber.right.toString())
        result.WriteString("]")
        return result.String()
    }
}

func (v1 *SnailNumber) add(v2 *SnailNumber) *SnailNumber {
    result := SnailNumber{
        left: v1,
        right: v2,
    }
    v1.parent = &result
    v2.parent = &result
    result.reduce()
    return &result
}

func (snailNumber *SnailNumber) reduce() {
    didReduce := true
    for didReduce {
        atDepth := snailNumber.getAtDepth(4)
        if atDepth != nil {
            atDepth.explode()
        } else {
            minValue := snailNumber.getWithMinValue(10)
            if minValue != nil {
                minValue.split()
            } else {
                didReduce = false
            }
        }
    }
}

func (snailNumber *SnailNumber) getAtDepth(goal int) *SnailNumber {
    if snailNumber.isLeaf() {
        return nil
    } else if goal == 0 {
        return snailNumber
    } else {
        result := snailNumber.left.getAtDepth(goal-1)
        if result == nil {
            result = snailNumber.right.getAtDepth(goal-1)
        }
        return result
    }
}

func (snailNumber *SnailNumber) explode() {
    snailNumber.updateClosestNode(Left, snailNumber.left.value)
    snailNumber.updateClosestNode(Right, snailNumber.right.value)
    snailNumber.left = nil
    snailNumber.right = nil
}

type Direction int64

const (
	Left Direction = iota
	Right
)

func (snailNumber *SnailNumber) updateClosestNode(direction Direction, value int) {
    if snailNumber.isRoot() {
        return
    }

    closestNode := snailNumber.parent.right
    if direction == Left {
        closestNode = snailNumber.parent.left
    }
    
    if *snailNumber == *closestNode {
        snailNumber.parent.updateClosestNode(direction, value)
    } else {
        for !closestNode.isLeaf() {
            if direction == Left {
                closestNode = closestNode.right
            } else {
                closestNode = closestNode.left
            }
        }
        closestNode.value += value
    }
}

func (snailNumber *SnailNumber) getWithMinValue(goal int) *SnailNumber {
    if snailNumber.isLeaf() {
        result := snailNumber
        if snailNumber.value < goal {
            result = nil
        }
        return result
    } else {
        result := snailNumber.left.getWithMinValue(goal)
        if result == nil {
            result = snailNumber.right.getWithMinValue(goal)
        }
        return result
    }
}

func (snailNumber *SnailNumber) split() {
    newNode := SnailNumber{}
    newNode.parent = snailNumber.parent
    newNode.left = &SnailNumber{
        value: snailNumber.value / 2,
        parent: &newNode,
    }
    newNode.right = &SnailNumber{
        value: (snailNumber.value + 1) / 2,
        parent: &newNode,
    }
    *snailNumber = newNode
}

func (snailNumber *SnailNumber) magnitude() int {
    if snailNumber.isLeaf() {
        return snailNumber.value
    } else {
        leftValue := snailNumber.left.magnitude()
        rightValue := snailNumber.right.magnitude()
        return (3 * leftValue) + (2 * rightValue)
    }
}

func main() {
    rawNumbers := getData()

    // Part 1: 3892
    fmt.Printf("Part 1: %d \n", sumAll(rawNumbers))
    // Part 2: 4909
    fmt.Printf("Part 2: %d \n", sumAny(rawNumbers))
}

func sumAll(rawNumbers []string) int {
    sum := parseNumber(rawNumbers[0])
    for _, rawNumber := range rawNumbers[1:] {
        sum = sum.add(parseNumber(rawNumber))
    }
    return sum.magnitude()
}

func sumAny(rawNumbers []string) int {
    max := 0
    for i, v1 := range rawNumbers {
        for j, v2 := range rawNumbers {
            if i != j {
                sum := parseNumber(v1).add(parseNumber(v2))
                magnitude := sum.magnitude()
                if magnitude > max {
                    max = magnitude
                }
            }
        }
    }
    return max
}

func getData() []string {
    data, _ := ioutil.ReadFile("data.txt")
    return strings.Split(string(data), "\r\n")
}

func parseNumber(rawNumber string) *SnailNumber {
    return parse(rawNumber, nil)
}

func parse(rawNumber string, parent *SnailNumber) *SnailNumber {
    result := SnailNumber{}
    result.parent = parent
    if rawNumber[0] == '[' {
        unnested := rawNumber[1:len(rawNumber) - 1]
        split := getSplit(unnested)
        result.left = parse(unnested[:split], &result)
        result.right = parse(unnested[split + 1:], &result)
    } else {
        value, _ := strconv.Atoi(rawNumber)
        result.value = value
    }
    return &result
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
