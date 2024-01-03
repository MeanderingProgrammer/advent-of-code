package main

import (
	"advent-of-code/commons/go/answer"
	"advent-of-code/commons/go/file"
	"advent-of-code/commons/go/grid"
	"advent-of-code/commons/go/parser"
	"advent-of-code/commons/go/point"
	"advent-of-code/commons/go/util"
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
	grid     grid.Grid[int]
	marked   map[point.Point]bool
	order    []int
	complete bool
}

func (board *Board) mark(value int) {
	points := board.grid.GetPoints(value)
	if len(points) != 1 {
		return
	}
	p := points[0]

	board.marked[p] = true
	board.order = append(board.order, value)

	rowComplete := board.isComplete(p, func(p point.Point) int { return p.Y })
	columnComplete := board.isComplete(p, func(p point.Point) int { return p.X })
	if rowComplete || columnComplete {
		board.complete = true
	}
}

func (board Board) isComplete(targetPoint point.Point, f func(point.Point) int) bool {
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
			total += board.grid.Get(point)
		}
	}
	lastMarked := board.order[len(board.order)-1]
	return total * lastMarked
}

func main() {
	order, boards := getData()

	scores := boards.runToComplete(order)
	answer.Part1(44088, scores[0])
	answer.Part2(23670, scores[len(scores)-1])
}

func getData() ([]int, Boards) {
	orderBoards := file.ReadGroups()
	return util.IntCsv(orderBoards[0]), parseBoards(orderBoards[1:])
}

func parseBoards(boards []string) Boards {
	var result Boards
	for _, board := range boards {
		grid := parser.GridMaker[int]{
			Rows:        util.Lines(board),
			Splitter:    parser.Field,
			Ignore:      "",
			Transformer: parser.ToInt,
		}.Construct()
		board := Board{
			grid:     grid,
			marked:   make(map[point.Point]bool),
			order:    nil,
			complete: false,
		}
		result = append(result, &board)
	}
	return result
}
