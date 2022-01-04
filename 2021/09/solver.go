package main

import (
	"advent-of-code/commons/go/answers"
	"advent-of-code/commons/go/conversions"
	"advent-of-code/commons/go/files"
	"advent-of-code/commons/go/parsers"
	"sort"
)

type Points []parsers.Point

func (points Points) contains(point parsers.Point) bool {
	for _, contained := range points {
		if contained == point {
			return true
		}
	}
	return false
}

func (points Points) riskLevel(grid parsers.Grid) int {
	result := 0
	for _, point := range points {
		result += conversions.ToInt(grid.Get(point)) + 1
	}
	return result
}

func (points Points) basinSizes(grid parsers.Grid) []int {
	var basinSizes []int
	for _, point := range points {
		basinSizes = append(basinSizes, basinSize(grid, point))
	}
	return basinSizes
}

func basinSize(grid parsers.Grid, point parsers.Point) int {
	basin := Points{point}
	for i := 0; i < len(basin); i++ {
		for _, adjacent := range basin[i].Adjacent(false) {
			adjacentValue, exists := grid.Get(adjacent), grid.Contains(adjacent)
			if exists && conversions.ToInt(adjacentValue) < 9 && !basin.contains(adjacent) {
				basin = append(basin, adjacent)
			}
		}
	}
	return len(basin)
}

func main() {
	grid := getGrid()

	minimums := minimums(grid)
	answers.Part1(506, minimums.riskLevel(grid))

	basinSizes := minimums.basinSizes(grid)
	sort.Sort(sort.Reverse(sort.IntSlice(basinSizes)))
	answers.Part2(931200, basinSizes[0]*basinSizes[1]*basinSizes[2])
}

func minimums(grid parsers.Grid) Points {
	var result Points
	for _, point := range grid.Points() {
		if isMinimum(grid, point) {
			result = append(result, point)
		}
	}
	return result
}

func isMinimum(grid parsers.Grid, point parsers.Point) bool {
	value := conversions.ToInt(grid.Get(point))
	for _, adjacent := range point.Adjacent(false) {
		adjacentValue, exists := grid.Get(adjacent), grid.Contains(adjacent)
		if exists && conversions.ToInt(adjacentValue) <= value {
			return false
		}
	}
	return true
}

func getGrid() parsers.Grid {
	return parsers.ConstructGrid(files.ReadLines(), parsers.Character, "")
}
