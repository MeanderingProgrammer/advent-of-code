package main

import (
	"advent-of-code/commons/go/answer"
	"advent-of-code/commons/go/file"
	"advent-of-code/commons/go/util"
)

type SnailNumber struct {
	value  int
	parent *SnailNumber
	left   *SnailNumber
	right  *SnailNumber
}

func (number *SnailNumber) isRoot() bool {
	return number.parent == nil
}

func (number *SnailNumber) isLeaf() bool {
	return number.left == nil && number.right == nil
}

func (v1 *SnailNumber) add(v2 *SnailNumber) *SnailNumber {
	result := SnailNumber{
		left:  v1,
		right: v2,
	}
	v1.parent = &result
	v2.parent = &result
	result.reduce()
	return &result
}

func (number *SnailNumber) reduce() {
	didReduce := true
	for didReduce {
		atDepth := number.getAtDepth(4)
		if atDepth != nil {
			atDepth.explode()
		} else {
			minValue := number.getWithMinValue(10)
			if minValue != nil {
				minValue.split()
			} else {
				didReduce = false
			}
		}
	}
}

func (number *SnailNumber) getAtDepth(goal int) *SnailNumber {
	if number.isLeaf() {
		return nil
	} else if goal == 0 {
		return number
	} else {
		result := number.left.getAtDepth(goal - 1)
		if result == nil {
			result = number.right.getAtDepth(goal - 1)
		}
		return result
	}
}

func (number *SnailNumber) explode() {
	number.updateClosestNode(Left, number.left.value)
	number.updateClosestNode(Right, number.right.value)
	number.left = nil
	number.right = nil
}

type Direction int64

const (
	Left Direction = iota
	Right
)

func (number *SnailNumber) updateClosestNode(direction Direction, value int) {
	if number.isRoot() {
		return
	}

	closestNode := number.parent.right
	if direction == Left {
		closestNode = number.parent.left
	}

	if *number == *closestNode {
		number.parent.updateClosestNode(direction, value)
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

func (number *SnailNumber) getWithMinValue(goal int) *SnailNumber {
	if number.isLeaf() {
		result := number
		if number.value < goal {
			result = nil
		}
		return result
	} else {
		result := number.left.getWithMinValue(goal)
		if result == nil {
			result = number.right.getWithMinValue(goal)
		}
		return result
	}
}

func (number *SnailNumber) split() {
	newNode := SnailNumber{}
	newNode.parent = number.parent
	newNode.left = &SnailNumber{
		value:  number.value / 2,
		parent: &newNode,
	}
	newNode.right = &SnailNumber{
		value:  (number.value + 1) / 2,
		parent: &newNode,
	}
	*number = newNode
}

func (number *SnailNumber) magnitude() int {
	if number.isLeaf() {
		return number.value
	} else {
		leftValue := number.left.magnitude()
		rightValue := number.right.magnitude()
		return (3 * leftValue) + (2 * rightValue)
	}
}

func main() {
	answer.Timer(solution)
}

func solution() {
	numbers := file.Default[string]().ReadLines()
	answer.Part1(3892, sumAll(numbers))
	answer.Part2(4909, sumAny(numbers))
}

func sumAll(numbers []string) int {
	sum := parse(numbers[0], nil)
	for _, number := range numbers[1:] {
		sum = sum.add(parse(number, nil))
	}
	return sum.magnitude()
}

func sumAny(numbers []string) int {
	result := 0
	for i, v1 := range numbers {
		for j, v2 := range numbers {
			if i != j {
				sum := parse(v1, nil).add(parse(v2, nil))
				result = max(result, sum.magnitude())
			}
		}
	}
	return result
}

func parse(rawNumber string, parent *SnailNumber) *SnailNumber {
	result := SnailNumber{}
	result.parent = parent
	if rawNumber[0] == '[' {
		unnested := rawNumber[1 : len(rawNumber)-1]
		left, right := util.SplitAt(unnested, getSplit(unnested))
		result.left = parse(left, &result)
		result.right = parse(right, &result)
	} else {
		result.value = util.ToInt(rawNumber)
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
	panic("Could not find location to split")
}
