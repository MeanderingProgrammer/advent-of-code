package main

import (
	"advent-of-code/commons/go/answer"
	"advent-of-code/commons/go/file"
	"advent-of-code/commons/go/util"
	"strings"
)

type Position struct {
	horizontal int
	depth      int
	aim        int
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
	amount    int
}

type Instructions []Instruction

func (instructions Instructions) follow(f func(*Position, int, Direction)) int {
	position := &Position{}
	for _, instruction := range instructions {
		f(position, instruction.amount, instruction.direction)
	}
	return position.magicNumber()
}

func main() {
	answer.Timer(solution)
}

func solution() {
	instructions := getInstructions()
	answer.Part1(1459206, instructions.follow(part1))
	answer.Part2(1320534480, instructions.follow(part2))
}

func getInstructions() Instructions {
	toInstruction := func(line string) Instruction {
		parts := strings.Fields(line)
		return Instruction{
			direction: Direction(parts[0]),
			amount:    util.ToInt(parts[1]),
		}
	}
	return file.Default[Instruction]().Read(toInstruction)
}

func part1(position *Position, amount int, direction Direction) {
	switch direction {
	case Forward:
		position.horizontal += amount
	case Down:
		position.depth += amount
	case Up:
		position.depth -= amount
	}
}

func part2(position *Position, amount int, direction Direction) {
	switch direction {
	case Forward:
		{
			position.horizontal += amount
			position.depth += (position.aim * amount)
		}
	case Down:
		position.aim += amount
	case Up:
		position.aim -= amount
	}
}
