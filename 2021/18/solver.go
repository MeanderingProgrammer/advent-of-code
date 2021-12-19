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

func (snailNumber SnailNumber) isLeaf() bool {
    return snailNumber.left == nil && snailNumber.right == nil
}

func (snailNumber SnailNumber) toString() string {
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
    result := SnailNumber{}
    
    result.left = v1
    v1.parent = &result
    
    result.right = v2
    v2.parent = &result

    return result.reduce()
}

type Direction int64

const (
	Left Direction = iota
	Right
)

func (direction Direction) getNumber(snailNumber *SnailNumber) *SnailNumber {
    if direction == Left {
        return snailNumber.left
    } else {
        return snailNumber.right
    }
}

func (direction Direction) getOpposite(snailNumber *SnailNumber) *SnailNumber {
    if direction == Left {
        return snailNumber.right
    } else {
        return snailNumber.left
    }
}

func (snailNumber *SnailNumber) reduce() *SnailNumber {
    didExplode, didSplit := true, true
    for didExplode || didSplit {
        didExplode = snailNumber.explode()
        if !didExplode {
            didSplit = snailNumber.split()
        }
    }
    return snailNumber
}

func (snailNumber *SnailNumber) explode() bool {
    atDepth := snailNumber.getAtDepth(0, 4)
    if atDepth == nil {
        return false
    }

    toLeft := atDepth.get(Left)
    if toLeft != nil {
        newValue := SnailNumber{}
        newValue.value = toLeft.value + atDepth.left.value
        newValue.parent = toLeft.parent
        *toLeft = newValue
    }

    toRight := atDepth.get(Right)
    if toRight != nil {
        newValue := SnailNumber{}
        newValue.value = toRight.value + atDepth.right.value
        newValue.parent = toRight.parent
        *toRight = newValue
    }

    newNode := SnailNumber{}
    newNode.parent = atDepth.parent
    *atDepth = newNode

    return true
}

func (snailNumber *SnailNumber) getAtDepth(current int, goal int) *SnailNumber {
    if snailNumber.isLeaf() {
        return nil
    } else if current == goal {
        return snailNumber
    } else {
        fromLeft := snailNumber.left.getAtDepth(current + 1, goal)
        if fromLeft != nil {
            return fromLeft
        } else {
            return snailNumber.right.getAtDepth(current + 1, goal)
        }
    }
}

func (snailNumber *SnailNumber) get(direction Direction) *SnailNumber {
    if snailNumber.parent == nil {
        return nil
    }
    
    numberInDirection := direction.getNumber(snailNumber.parent)
    if *snailNumber == *numberInDirection {
        return snailNumber.parent.get(direction)
    } else {
        for !numberInDirection.isLeaf() {
            numberInDirection = direction.getOpposite(numberInDirection)
        }
        return numberInDirection
    }
}

func (snailNumber *SnailNumber) split() bool {
    minValue := snailNumber.getWithMinValue(10)
    if minValue == nil {
        return false
    }

    newNode := SnailNumber{}
    newNode.parent = minValue.parent
    newNode.left = &SnailNumber{
        value: minValue.value / 2,
        parent: &newNode,
    }
    newNode.right = &SnailNumber{
        value: (minValue.value + 1) / 2,
        parent: &newNode,
    }

    *minValue = newNode

    return true
}

func (snailNumber *SnailNumber) getWithMinValue(goal int) *SnailNumber {
    if snailNumber.isLeaf() {
        if snailNumber.value >= goal {
            return snailNumber
        } else {
            return nil
        }
    } else {
        fromLeft := snailNumber.left.getWithMinValue(goal)
        if fromLeft != nil {
            return fromLeft
        } else {
            return snailNumber.right.getWithMinValue(goal)
        }
    }
}

func (snailNumber SnailNumber) magnitude() int {
    if snailNumber.isLeaf() {
        return snailNumber.value
    } else {
        leftValue := snailNumber.left.magnitude()
        rightValue := snailNumber.right.magnitude()
        return (3 * leftValue) + (2 * rightValue)
    }
}

func main() {
    numbers := getData()

    fmt.Printf("Part 1 = %d \n", sumAll(numbers))
    fmt.Printf("Part 2 = %d \n", sumAny(numbers))
}

func sumAll(numbers []*SnailNumber) int {
    sum := numbers[0]
    for _, value := range numbers[1:] {
        sum = sum.add(value)
    }
    return sum.magnitude()
}

func sumAny(numbers []*SnailNumber) int {
    max, length := 0, len(numbers)
    for i := 0; i < length; i++ {
        for j := 0; j < length; j++ {
            if i != j {
                magnitude := getData()[i].add(getData()[j]).magnitude()
                if magnitude > max {
                    max = magnitude
                }
            }
        }
    }
    return max
}

func getData() []*SnailNumber {
    data, _ := ioutil.ReadFile("data.txt")
    rawNumbers := strings.Split(string(data), "\r\n")
    var result []*SnailNumber
    for _, rawNumber := range rawNumbers {
        snailNumber := parseSnailNumber(rawNumber, nil)
        result = append(result, snailNumber)
    }
    return result
}

func parseSnailNumber(rawNumber string, parent *SnailNumber) *SnailNumber {
    result := SnailNumber{}
    result.parent = parent
    if rawNumber[0] == '[' {
        unnested := rawNumber[1:len(rawNumber) - 1]
        split := getSplit(unnested)
        result.left = parseSnailNumber(unnested[:split], &result)
        result.right = parseSnailNumber(unnested[split + 1:], &result)
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
