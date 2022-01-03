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
    graph parsers.Graph
    marked map[parsers.Point]bool
    order []int
    complete bool
}

func (board *Board) mark(value int) {
    point, exists := board.graph.GetPoint(conversions.ToString(value))
    if !exists {
        return
    }

    board.marked[point] = true
    board.order = append(board.order, value)

    rowComplete := board.isComplete(point, func(p parsers.Point) int {return p.Y})
    columnComplete := board.isComplete(point, func(p parsers.Point) int {return p.X})
    if rowComplete || columnComplete {
        board.complete = true
    }
}

func (board Board) isComplete(targetPoint parsers.Point, f func(parsers.Point) int) bool {
    targetCoord := f(targetPoint)
    for point := range board.graph.Grid {
        if f(point) == targetCoord && !board.marked[point] {
            return false
        }
    }
    return true
}

func (board Board) score() int {
    total := 0
    for point, value := range board.graph.Grid {
        if !board.marked[point] {
            total += conversions.ToInt(value)
        }
    }
    lastMarked := board.order[len(board.order) - 1]
    return total * lastMarked
}

func main() {
    order, boards := getData()

    scores := boards.runToComplete(order)
    answers.Part1(44088, scores[0])
    answers.Part2(23670, scores[len(scores) - 1])
}

func getData() ([]int, Boards) {
    orderBoards := files.ReadGroups()
    return parsers.IntCsv(orderBoards[0]), parseBoards(orderBoards[1:])
}

func parseBoards(boards []string) Boards {
    var result Boards
    for _, board := range boards {
        graph := parsers.ConstructGraph(board, parsers.Field, "")
        board := Board{
            graph: graph,
            marked: make(map[parsers.Point]bool),
            order: nil,
            complete: false,
        }
        result = append(result, &board)
    }
    return result
}
