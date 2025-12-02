package main

import (
	"fmt"
	"strings"

	"advent-of-code/commons/go/answer"
	"advent-of-code/commons/go/file"
	"advent-of-code/commons/go/util"
)

// Refactored Input + Details
//
// zs:  [1  1   1   26  1   26  1   1   26  1   26  26  26  26  ]
// xs:  [12 15  11  -14 12  -10 11  13  -7  10  -2  -1  -4  -12 ]
// ys:  [4  11  7   2   11  13  9   12  6   2   11  12  3   13  ]
//
// inp w        w = in[i]               w = in[i]
// mul x 0      x = 0                   x = 0
// add x z      x += z                  x = z
// mod x 26     x %= 26                 x = z % 26
// div z zs     z /= zs[i]              z /= zs[i]
// add x xs     x += xs[i]              x = (z % 26) + xs[i]
// eql x w      x = (x == w) ? 1 : 0    x = ((z % 26) + xs[i] == in[i]) ? 1 : 0
// eql x 0      x = (x == 0) ? 1 : 0    x = ((z % 26) + xs[i] != in[i]) ? 1 : 0
// mul y 0      y = 0                   y = 0
// add y 25     y += 25                 y = 25
// mul y x      y *= x                  y = ((z % 26) + xs[i] != in[i]) ? 25 : 0
// add y 1      y += 1                  y = ((z % 26) + xs[i] != in[i]) ? 26 : 1
// mul z y      z *= y                  z *= ((z % 26) + xs[i] != in[i]) ? 26 : 1
// mul y 0      y = 0                   y = 0
// add y w      y += w                  y = in[i]
// add y ys     y += ys[i]              y = in[i] + ys[i]
// mul y x      y *= x                  y = ((z % 26) + xs[i] != in[i]) ? in[i] + ys[i] : 0
// add z y      z += y                  z += ((z % 26) + xs[i] != in[i]) ? in[i] + ys[i] : 0
//
// Notes
//   - On iterations where xs[i] > 9, we cannot avoid increasing the value of z
//   - On iterations where we must increase z (xs[i] > 9) we multiply by a factor of 26
//   - There are 7 such occurrences in our input dataset
//   - We divide z by 26 based on the value of zs[i] exactly 7 times as well
//   - If we avoid the factor of 26 increase on iterations where we can, we will reduce z to 0
//   - This is done by getting z to an appropraite value such that (z % 26) + xs[i] equals our
//     input at that iteration, also note that xs[i] on these iterations is negative
//
// Solution
// - Relies on which indexes of the input the z calculation is based on, nearest unassigned neighbor
// - zs:        1   1   1   26  1   26  1   1   26  1   26  26  26  26
// - group:     1   2   3   3   4   4   5   6   6   7   7   5   2   1
func main() {
	answer.Timer(solution)
}

func solution() {
	program := getProgram()
	constrainedNumber := addConstraints(
		group(program.nth(4)),
		program.nth(15),
		program.nth(5),
	)
	answer.Part1(92928914999991, constrainedNumber.bound(true))
	answer.Part2(91811211611981, constrainedNumber.bound(false))
}

type ConstrainedNumber []ConstrainedPair

func (number ConstrainedNumber) bound(max bool) int {
	result := make([]int, len(number)*2)
	for _, constraint := range number {
		var startValue, endValue int
		startToEnd := constraint.startToEnd
		if startToEnd < 0 {
			if max {
				startValue, endValue = 9, 9+startToEnd
			} else {
				startValue, endValue = 1-startToEnd, 1
			}
		} else {
			if max {
				startValue, endValue = 9-startToEnd, 9
			} else {
				startValue, endValue = 1, 1+startToEnd
			}
		}
		result[constraint.start] = startValue
		result[constraint.end] = endValue
	}
	return parseResult(result)
}

type ConstrainedPair struct {
	start      int
	end        int
	startToEnd int
}

func addConstraints(groups map[int]int, startOffsets []int, endOffsets []int) ConstrainedNumber {
	var result []ConstrainedPair
	for start, end := range groups {
		startToEnd := startOffsets[start] + endOffsets[end]
		constrainedPair := ConstrainedPair{start, end, startToEnd}
		result = append(result, constrainedPair)
	}
	return result
}

func group(pairing []int) map[int]int {
	groups := make(map[int]int)
	for i, value := range pairing {
		if value == 26 {
			start := closestUnpaired(pairing[:i], groups)
			groups[start] = i
		}
	}
	return groups
}

func closestUnpaired(before []int, existing map[int]int) int {
	for i := len(before) - 1; i >= 0; i-- {
		value := before[i]
		if value == 1 {
			_, alreadyPaired := existing[i]
			if !alreadyPaired {
				return i
			}
		}
	}
	panic("Should always be able to find a pair")
}

type Instruction []string

type Program []Instruction

func (program Program) nth(n int) []int {
	var values []int
	for i, instruction := range program {
		if i%18 == n {
			values = append(values, util.ToInt(instruction[2]))
		}
	}
	return values
}

func getProgram() Program {
	var program []Instruction
	for _, rawInstruction := range file.Default().Lines() {
		instruction := strings.Split(rawInstruction, " ")
		program = append(program, instruction)
	}
	return program
}

func parseResult(values []int) int {
	var result strings.Builder
	for _, value := range values {
		result.WriteString(util.ToString(value))
	}
	return util.ToInt(result.String())
}

// ================================================================================================
// Below implements the programatic way to solve this problem, parsing input and storing values
// in the ALU struct registers
// It is really slow and in the time it takes to optimize this based on the input, it is faster
// to implement an analytical solution, details above main()
// It was helpful in validating the behavior of the analytical solution by printing out register
// values for different test inputs
// ================================================================================================

type InputProvider struct {
	source string
	index  int
}

func (provider *InputProvider) next() string {
	value := string(provider.source[provider.index])
	provider.index++
	return value
}

type ALU struct {
	w int
	x int
	y int
	z int
}

func (alu *ALU) runProgram(program Program, provider *InputProvider) int {
	for i, instruction := range program {
		alu.runInstruction(instruction, provider)
		// For debugging purposes
		fmt.Printf("Instruction Set: %d, Number %d\n", (i/18)+1, (i%18)+1)
		fmt.Println(instruction)
		fmt.Println(*alu)
	}
	return alu.z
}

func (alu *ALU) runInstruction(instruction Instruction, provider *InputProvider) {
	operation, r1 := instruction[0], instruction[1]

	var r2 string
	if operation == "inp" {
		r2 = provider.next()
	} else {
		r2 = instruction[2]
	}
	r2Value := alu.get(r2)

	var result int
	switch operation {
	case "inp":
		result = r2Value
	case "add":
		r1Value := alu.get(r1)
		result = r1Value + r2Value
	case "mul":
		r1Value := alu.get(r1)
		result = r1Value * r2Value
	case "div":
		r1Value := alu.get(r1)
		result = r1Value / r2Value
	case "mod":
		r1Value := alu.get(r1)
		result = r1Value % r2Value
	case "eql":
		r1Value := alu.get(r1)
		if r1Value == r2Value {
			result = 1
		} else {
			result = 0
		}
	default:
		panic(fmt.Sprintf("Unkown operation: %s", operation))
	}
	alu.set(r1, result)
}

func (alu *ALU) set(register string, value int) {
	switch register {
	case "w":
		alu.w = value
	case "x":
		alu.x = value
	case "y":
		alu.y = value
	case "z":
		alu.z = value
	default:
		panic(fmt.Sprintf("Unkown register: %s", register))
	}
}

func (alu *ALU) get(register string) int {
	var value int
	switch register {
	case "w":
		value = alu.w
	case "x":
		value = alu.x
	case "y":
		value = alu.y
	case "z":
		value = alu.z
	default:
		value = util.ToInt(register)
	}
	return value
}

func runSlow(source int) int {
	program := getProgram()
	alu := ALU{}
	provider := InputProvider{
		source: util.ToString(source),
	}
	return alu.runProgram(program, &provider)
}
