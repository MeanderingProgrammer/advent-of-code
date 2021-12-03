package main

import(
    "fmt"
	"io/ioutil"
	"strings"
	"strconv"
)

type Position struct {
    horizontal int
    depth  int
	aim int
}

func (position Position) magicNumber() int {
	return position.depth * position.horizontal
}

type Direction string

const (
	Forward Direction = "forward"
	Down              = "down"
	Up                = "up"
)

type Instruction struct {
	direction Direction
	amount int
}

type Instructions []Instruction

func (instructions Instructions) follow(f func(*Position, Instruction)) Position {
	position := Position{}
	for _, instruction := range instructions {
		f(&position, instruction)
	}
	return position
}

func main() {
	instructions := getInstructions()
	position1 := instructions.follow(move1)
	position2 := instructions.follow(move2)

	fmt.Printf("Part 1 = %d \n", position1.magicNumber())
	fmt.Printf("Part 2 = %d \n", position2.magicNumber())
}

func getInstructions() Instructions {
	var instructions Instructions

	content, _ := ioutil.ReadFile("data.txt")
    lines := strings.Split(string(content), "\r\n")
	for _, line := range lines {
		parts := strings.Split(line, " ")
		amount, _ := strconv.Atoi(parts[1])
		instruction := Instruction{Direction(parts[0]), amount}
		instructions = append(instructions, instruction)
	}

	return instructions
}

func move1(position *Position, instruction Instruction) {
	amount := instruction.amount
	switch instruction.direction {
	case Forward: position.horizontal += amount
	case Down: position.depth += amount
	case Up: position.depth -= amount
	}
}

func move2(position *Position, instruction Instruction) {
	amount := instruction.amount
	switch instruction.direction {
	case Forward: {
		position.horizontal += amount
		position.depth += (position.aim * amount)
	}
	case Down: position.aim += amount
	case Up: position.aim -= amount
	}
}
