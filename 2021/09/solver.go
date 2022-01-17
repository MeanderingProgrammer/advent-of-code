package main

import (
	"advent-of-code/commons/go/answers"
	"advent-of-code/commons/go/conversions"
	"advent-of-code/commons/go/files"
	"advent-of-code/commons/go/parsers"
	"advent-of-code/commons/go/utils"
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

func (points Points) riskLevel(grid Grid) int {
	result := 0
	for _, point := range points {
		result += grid.Get(point) + 1
	}
	return result
}

func (points Points) basinSizes(grid Grid) []int {
	var basinSizes []int
	for _, point := range points {
		basinSizes = append(basinSizes, basinSize(grid, point))
	}
	return basinSizes
}

func basinSize(grid Grid, point parsers.Point) int {
	basin := Points{point}
	for i := 0; i < len(basin); i++ {
		for _, adjacent := range basin[i].Adjacent(false) {
			if grid.Contains(adjacent) && grid.Get(adjacent) < 9 && !basin.contains(adjacent) {
				basin = append(basin, adjacent)
			}
		}
	}
	return len(basin)
}

type Grid struct {
	parsers.Grid[int]
}

func (grid Grid) minimums() Points {
	isMinimum := func(point parsers.Point) bool {
		value := grid.Get(point)
		for _, adjacent := range point.Adjacent(false) {
			if grid.Contains(adjacent) && grid.Get(adjacent) <= value {
				return false
			}
		}
		return true
	}
	return utils.Filter(grid.Points(), isMinimum)
}

func main() {
	grid := getGrid()

	minimums := grid.minimums()
	answers.Part1(506, minimums.riskLevel(grid))

	basinSizes := minimums.basinSizes(grid)
	sort.Sort(sort.Reverse(sort.IntSlice(basinSizes)))
	answers.Part2(931200, basinSizes[0]*basinSizes[1]*basinSizes[2])
}

func getGrid() Grid {
	toInt := func(point parsers.Point, value string) int {
		return conversions.ToInt(value)
	}
	grid := parsers.GridMaker[int]{
		Rows:        files.ReadLines(),
		Splitter:    parsers.Character,
		Ignore:      "",
		Transformer: toInt,
	}.Construct()
	return Grid{grid}
}
