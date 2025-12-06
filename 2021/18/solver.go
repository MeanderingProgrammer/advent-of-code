package main

import (
	"advent-of-code/lib/go/answer"
	"advent-of-code/lib/go/file"
	"advent-of-code/lib/go/util"
)

type SnailNumber struct {
	value  int
	parent *SnailNumber
	left   *SnailNumber
	right  *SnailNumber
}

func (n *SnailNumber) isRoot() bool {
	return n.parent == nil
}

func (n *SnailNumber) isLeaf() bool {
	return n.left == nil && n.right == nil
}

func (n *SnailNumber) add(other *SnailNumber) *SnailNumber {
	result := SnailNumber{
		left:  n,
		right: other,
	}
	n.parent = &result
	other.parent = &result
	result.reduce()
	return &result
}

func (n *SnailNumber) reduce() {
	didReduce := true
	for didReduce {
		atDepth := n.getAtDepth(4)
		if atDepth != nil {
			atDepth.explode()
		} else {
			minValue := n.getWithMinValue(10)
			if minValue != nil {
				minValue.split()
			} else {
				didReduce = false
			}
		}
	}
}

func (n *SnailNumber) getAtDepth(goal int) *SnailNumber {
	if n.isLeaf() {
		return nil
	} else if goal == 0 {
		return n
	} else {
		result := n.left.getAtDepth(goal - 1)
		if result == nil {
			result = n.right.getAtDepth(goal - 1)
		}
		return result
	}
}

func (n *SnailNumber) explode() {
	n.updateClosestNode(Left, n.left.value)
	n.updateClosestNode(Right, n.right.value)
	n.left = nil
	n.right = nil
}

type Direction int64

const (
	Left Direction = iota
	Right
)

func (n *SnailNumber) updateClosestNode(direction Direction, value int) {
	if n.isRoot() {
		return
	}

	closestNode := n.parent.right
	if direction == Left {
		closestNode = n.parent.left
	}

	if *n == *closestNode {
		n.parent.updateClosestNode(direction, value)
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

func (n *SnailNumber) getWithMinValue(goal int) *SnailNumber {
	if n.isLeaf() {
		result := n
		if n.value < goal {
			result = nil
		}
		return result
	} else {
		result := n.left.getWithMinValue(goal)
		if result == nil {
			result = n.right.getWithMinValue(goal)
		}
		return result
	}
}

func (n *SnailNumber) split() {
	newNode := SnailNumber{}
	newNode.parent = n.parent
	newNode.left = &SnailNumber{
		value:  n.value / 2,
		parent: &newNode,
	}
	newNode.right = &SnailNumber{
		value:  (n.value + 1) / 2,
		parent: &newNode,
	}
	*n = newNode
}

func (n *SnailNumber) magnitude() int {
	if n.isLeaf() {
		return n.value
	} else {
		leftValue := n.left.magnitude()
		rightValue := n.right.magnitude()
		return (3 * leftValue) + (2 * rightValue)
	}
}

func main() {
	answer.Timer(solution)
}

func solution() {
	numbers := file.Default().Lines()
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
