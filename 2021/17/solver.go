package main

import(
    "fmt"
    "io/ioutil"
    "strconv"
    "strings"
)

type TargetArea struct {
    xRange [2]int
    yRange [2]int
}

func (targetArea TargetArea) minStepsToReach() int {
    // If we start with an x velocity of 6 the max position we can reach
    // is 21 before we slow down to 0, hence we should not check anything
    // below 6
    sum, step := 0, 0
    for sum < targetArea.xRange[0] {
        step++
        sum += step
    }
    return step
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
    return trajectory[len(trajectory) - 2].in(targetArea)
}

func (trajectory Trajectory) overshot(targetArea TargetArea) bool {
    return trajectory[len(trajectory) - 1].over(targetArea)
}

func (trajectory Trajectory) maxHeight() int {
    max := trajectory[0].y
    for _, position := range trajectory[1:] {
        if position.y <= max {
            return max
        } else {
            max = position.y
        }
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

    // 990 is too low
    fmt.Printf("Part 1 = %d \n", getMaxHeight(targetArea))
}

func getMaxHeight(targetArea TargetArea) int {
    maxHeight := 0
    for x := targetArea.minStepsToReach(); x < targetArea.xRange[0]; x++ {
        fmt.Println(x)
        y := firstIn(targetArea, x)
        if y < 0 {
            return maxHeight
        }

        trajectory := targetArea.shoot(Velocity{x, y})
        fmt.Println(y)
        fmt.Println(trajectory)
        for trajectory.in(targetArea) {
            fmt.Println(trajectory.maxHeight())
            if trajectory.maxHeight() > maxHeight {
                maxHeight = trajectory.maxHeight()
            }
            y++
            trajectory = targetArea.shoot(Velocity{x, y})
            fmt.Println(y)
            fmt.Println(trajectory)
        }
    }
    return maxHeight
}

func firstIn(targetArea TargetArea, x int) int {
    for y := 0; y < 100; y++ {
        trajectory := targetArea.shoot(Velocity{x, y})
        if trajectory.in(targetArea) {
            return y
        }
    }
    return -1
}

func getData() TargetArea {
    data, _ := ioutil.ReadFile("data.txt")
    rawTargetArea := strings.Split(string(data), ": ")[1]
    components := strings.Split(rawTargetArea, ", ")
    return TargetArea{
        xRange: parseRange(components[0]),
        yRange: parseRange(components[1]),
    }
}


func parseRange(raw string) [2]int {
    values := strings.Split(raw, "=")[1]
    minxMax := strings.Split(values, "..")
    min, _ := strconv.Atoi(minxMax[0])
    max, _ := strconv.Atoi(minxMax[1])
    return [2]int{min, max}
}
