package main

import (
	"advent-of-code/commons/go/answers"
	"advent-of-code/commons/go/conversions"
	"advent-of-code/commons/go/files"
	"advent-of-code/commons/go/parsers"
)

type Boards []*Board

func (boards Boards) runToComplete(order []int) []int {
	var result []int
	for _, value := range order {
		for _, board := range boards.incomplete() {
			board.mark(value)
			if board.complete {
				result = append(result, board.score())
			}
		}
	}
	return result
}

func (boards Boards) incomplete() Boards {
	var result Boards
	for _, board := range boards {
		if !board.complete {
			result = append(result, board)
		}
	}
	return result
}

type Board struct {
	grid     parsers.Grid
	marked   map[parsers.Point]bool
	order    []int
	complete bool
}

func (board *Board) mark(value int) {
	points := board.grid.GetPoints(conversions.ToString(value))
	if len(points) != 1 {
		return
	}
	point := points[0]

	board.marked[point] = true
	board.order = append(board.order, value)

	rowComplete := board.isComplete(point, func(p parsers.Point) int { return p.Y })
	columnComplete := board.isComplete(point, func(p parsers.Point) int { return p.X })
	if rowComplete || columnComplete {
		board.complete = true
	}
}

func (board Board) isComplete(targetPoint parsers.Point, f func(parsers.Point) int) bool {
	targetCoord := f(targetPoint)
	for _, point := range board.grid.Points() {
		if f(point) == targetCoord && !board.marked[point] {
			return false
		}
	}
	return true
}

func (board Board) score() int {
	total := 0
	for _, point := range board.grid.Points() {
		if !board.marked[point] {
			total += conversions.ToInt(board.grid.Get(point))
		}
	}
	lastMarked := board.order[len(board.order)-1]
	return total * lastMarked
}

func main() {
	order, boards := getData()

	scores := boards.runToComplete(order)
	answers.Part1(44088, scores[0])
	answers.Part2(23670, scores[len(scores)-1])
}

func getData() ([]int, Boards) {
	orderBoards := files.ReadGroups()
	return parsers.IntCsv(orderBoards[0]), parseBoards(orderBoards[1:])
}

func parseBoards(boards []string) Boards {
	var result Boards
	for _, board := range boards {
		grid := parsers.ConstructGrid(parsers.Lines(board), parsers.Field, "")
		board := Board{
			grid:     grid,
			marked:   make(map[parsers.Point]bool),
			order:    nil,
			complete: false,
		}
		result = append(result, &board)
	}
	return result
}
