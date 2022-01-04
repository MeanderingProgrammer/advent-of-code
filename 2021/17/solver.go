package main

import (
	"advent-of-code/commons/go/answers"
	"advent-of-code/commons/go/conversions"
	"advent-of-code/commons/go/files"
	"advent-of-code/commons/go/parsers"
	"advent-of-code/commons/go/utils"
	"strings"
)

type TargetArea struct {
	xRange [2]int
	yRange [2]int
}

type Position struct {
	x int
	y int
}

func (position Position) move(velocity Velocity) Position {
	return Position{
		x: position.x + velocity.x,
		y: position.y + velocity.y,
	}
}

func (position Position) after(targetArea TargetArea) bool {
	return position.x > targetArea.xRange[1] || position.y < targetArea.yRange[0]
}

func (position Position) in(targetArea TargetArea) bool {
	afterMin := position.x >= targetArea.xRange[0] && position.y >= targetArea.yRange[0]
	beforeMax := position.x <= targetArea.xRange[1] && position.y <= targetArea.yRange[1]
	return afterMin && beforeMax
}

func (position Position) over(targetArea TargetArea) bool {
	return position.x > targetArea.xRange[1] && position.y > targetArea.yRange[0]
}

type Velocity Position

func (velocity Velocity) applyDrag() Velocity {
	x := velocity.x
	if x < 0 {
		x++
	} else if x > 0 {
		x--
	}
	return Velocity{x, velocity.y - 1}
}

type Trajectory []Position

func (trajectory Trajectory) in(targetArea TargetArea) bool {
	return trajectory[len(trajectory)-2].in(targetArea)
}

func (trajectory Trajectory) overshot(targetArea TargetArea) bool {
	return trajectory[len(trajectory)-1].over(targetArea)
}

func (trajectory Trajectory) maxHeight() int {
	max := 0
	for _, position := range trajectory {
		max = utils.Max(max, position.y)
	}
	return max
}

func (targetArea TargetArea) shoot(velocity Velocity) Trajectory {
	position := Position{0, 0}
	trajectory := Trajectory{position}
	for !position.after(targetArea) {
		position = position.move(velocity)
		velocity = velocity.applyDrag()
		trajectory = append(trajectory, position)
	}
	return trajectory
}

func main() {
	targetArea := getData()

	maxHeight, numValid := getMaxHeight(targetArea)
	answers.Part1(4095, maxHeight)
	answers.Part2(3773, numValid)
}

func getMaxHeight(targetArea TargetArea) (int, int) {
	maxHeight, numValid := 0, 0
	for x := 1; x <= targetArea.xRange[1]; x++ {
		for y := -100; y < 100; y++ {
			trajectory := targetArea.shoot(Velocity{x, y})
			if trajectory.in(targetArea) {
				numValid++
				maxHeight = utils.Max(maxHeight, trajectory.maxHeight())
			}
		}
	}
	return maxHeight, numValid
}

func getData() TargetArea {
	rawTargetArea := parsers.SubstringAfter(files.Content(), ": ")
	components := strings.Split(rawTargetArea, ", ")
	return TargetArea{
		xRange: parseRange(components[0]),
		yRange: parseRange(components[1]),
	}
}

func parseRange(raw string) [2]int {
	values := parsers.SubstringAfter(raw, "=")
	minxMax := strings.Split(values, "..")
	return [2]int{
		conversions.ToInt(minxMax[0]),
		conversions.ToInt(minxMax[1]),
	}
}
