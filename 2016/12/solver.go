package main

import (
	"advent-of-code/commons/go/answer"
	"advent-of-code/commons/go/file"
	"advent-of-code/commons/go/util"
	"strings"
)

type Computer struct {
	registers map[string]int
}

func NewComputer(registers []string) *Computer {
	computer := new(Computer)
	computer.registers = make(map[string]int)
	for _, register := range registers {
		computer.registers[register] = 0
	}
	return computer
}

func (c *Computer) get(register string) int {
	value, ok := c.registers[register]
	if ok {
		return value
	} else {
		return util.ToInt(register)
	}
}

func (c *Computer) set(register string, value int) {
	c.registers[register] = value
}

func (c *Computer) run(instructions []Instruction) {
	ip := 0
	for ip >= 0 && ip < len(instructions) {
		instruction := instructions[ip]
		ip += instruction.run(c)
	}
}

type Instruction interface {
	run(computer *Computer) int
}

type Copy struct {
	register string
	value    string
}

func (i *Copy) run(computer *Computer) int {
	computer.set(i.register, computer.get(i.value))
	return 1
}

type Increment struct {
	register string
	value    int
}

func (i *Increment) run(computer *Computer) int {
	computer.set(i.register, computer.get(i.register)+i.value)
	return 1
}

type Jump struct {
	register string
	value    int
}

func (i *Jump) run(computer *Computer) int {
	if computer.get(i.register) != 0 {
		return i.value
	} else {
		return 1
	}
}

func main() {
	instructions := file.Read(parseInstruction)
	answer.Part1(318117, run(instructions, false))
	answer.Part2(9227771, run(instructions, true))
}

func run(instructions []Instruction, ignite bool) int {
	computer := NewComputer([]string{"a", "b", "c", "d"})
	if ignite {
		computer.set("c", 1)
	}
	computer.run(instructions)
	return computer.get("a")
}

func parseInstruction(line string) Instruction {
	parts := strings.Split(line, " ")
	op := parts[0]
	if op == "cpy" {
		return &Copy{
			register: parts[2],
			value:    parts[1],
		}
	} else if op == "inc" {
		return &Increment{
			register: parts[1],
			value:    1,
		}
	} else if op == "dec" {
		return &Increment{
			register: parts[1],
			value:    -1,
		}
	} else if op == "jnz" {
		return &Jump{
			register: parts[1],
			value:    util.ToInt(parts[2]),
		}
	} else {
		panic("Unknown operation: " + op)
	}
}
