package main

import(
    "fmt"
    "io/ioutil"
    "sort"
    "strings"
    "strconv"
)

type Positions []int

func (positions Positions) difference(f func(int) int, value int) int {
    total := 0
    for _, position := range positions {
        difference := position - value
        total += f(difference)
    }
    return total
}

func main() {
    positions := getData()

    fmt.Printf("Part 1 = %d \n", minimize(positions, absolute))
    fmt.Printf("Part 2 = %d \n", minimize(positions, cumulative))

}

func absolute(difference int) int {
    if difference < 0 {
        difference *= -1
    }
    return difference
}

func cumulative(difference int) int {
    if difference < 0 {
        difference *= -1
    }
    return ((difference * difference) + difference) / 2
}

func getData() Positions {
    data, _ := ioutil.ReadFile("data.txt")
    rawPositions := strings.Split(string(data), ",")

    var positions []int
    for _, rawPosition := range rawPositions {
        position, _ := strconv.Atoi(rawPosition)
        positions = append(positions, position)
    }

    sort.Ints(positions)
    return positions
}

func minimize(positions Positions, f func(int) int) int {
    minimum := positions.difference(f, positions[0])
    for i := positions[0] + 1; i <= positions[len(positions) - 1]; i++ {
        value := positions.difference(f, i)
        if value < minimum {
            minimum = value
        }
    }
    return minimum
}
