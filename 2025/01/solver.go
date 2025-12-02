package main

import (
	"advent-of-code/commons/go/answer"
	"advent-of-code/commons/go/file"
	"advent-of-code/commons/go/util"
)

type Dial struct {
	value int
	size  int
}

func (d *Dial) move(right bool, amount int) int {
	// simplify full rotations
	clicks := amount / d.size
	amount %= d.size

	if right {
		d.value += amount
		if d.value >= d.size {
			d.value -= d.size
			clicks += 1
		}
	} else {
		if d.value > 0 && d.value <= amount {
			clicks += 1
		}
		d.value -= amount
		if d.value < 0 {
			d.value += d.size
		}
	}

	return clicks
}

func main() {
	answer.Timer(solution)
}

func solution() {
	lines := file.Default().Lines()

	zeros := 0
	clicks := 0
	dial := Dial{
		value: 50,
		size:  100,
	}
	for _, line := range lines {
		right := line[0] == 'R'
		amount := util.ToInt(line[1:])
		clicks += dial.move(right, amount)
		if dial.value == 0 {
			zeros += 1
		}
	}

	answer.Part1(1120, zeros)
	answer.Part2(6554, clicks)
}
