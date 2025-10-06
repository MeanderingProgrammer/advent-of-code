package main

import (
	"slices"
	"sort"

	"advent-of-code/commons/go/answer"
	"advent-of-code/commons/go/file"
	"advent-of-code/commons/go/grid"
	"advent-of-code/commons/go/parser"
	"advent-of-code/commons/go/point"
	"advent-of-code/commons/go/util"
)

type Points []point.Point

func (points Points) contains(p point.Point) bool {
	return slices.Contains(points, p)
}

func (points Points) riskLevel(g Grid) int {
	result := 0
	for _, point := range points {
		result += g.Get(point) + 1
	}
	return result
}

func (points Points) basinSizes(g Grid) []int {
	var basinSizes []int
	for _, point := range points {
		basinSizes = append(basinSizes, basinSize(g, point))
	}
	return basinSizes
}

func basinSize(g Grid, p point.Point) int {
	basin := Points{p}
	for i := 0; i < len(basin); i++ {
		for _, adjacent := range basin[i].Adjacent() {
			if g.Contains(adjacent) && g.Get(adjacent) < 9 && !basin.contains(adjacent) {
				basin = append(basin, adjacent)
			}
		}
	}
	return len(basin)
}

type Grid struct {
	grid.Grid[int]
}

func (g Grid) minimums() Points {
	isMinimum := func(p point.Point) bool {
		value := g.Get(p)
		for _, adjacent := range p.Adjacent() {
			if g.Contains(adjacent) && g.Get(adjacent) <= value {
				return false
			}
		}
		return true
	}
	return util.Filter(g.Points(), isMinimum)
}

func main() {
	answer.Timer(solution)
}

func solution() {
	grid := getGrid()

	minimums := grid.minimums()
	answer.Part1(506, minimums.riskLevel(grid))

	basinSizes := minimums.basinSizes(grid)
	sort.Sort(sort.Reverse(sort.IntSlice(basinSizes)))
	answer.Part2(931200, basinSizes[0]*basinSizes[1]*basinSizes[2])
}

func getGrid() Grid {
	grid := parser.GridMaker[int]{
		Rows:        file.Default[string]().ReadLines(),
		Splitter:    parser.Character,
		Ignore:      "",
		Transformer: parser.ToInt,
	}.Construct()
	return Grid{grid}
}
