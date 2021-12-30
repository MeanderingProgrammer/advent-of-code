package main

import(
    "fmt"
    "io/ioutil"
    "strings"
    "strconv"
)

type Position struct {
    row int
    column int
}

type Cell struct {
    value int
    marked bool
}

type Board struct {
    boardMap map[Position]*Cell
    numRows int
    numCols int
    complete *[]int
    markOrder []int
}

func (board *Board) mark(value int) {
    for position, cell := range board.boardMap {
        if (cell.value == value) {
            cell.marked = true
            board.markOrder = append(board.markOrder, value)

            completeRow := board.getComplete(position, func(pos Position) int {return pos.row})
            if completeRow != nil {
                board.complete = completeRow
            }

            completeColumn := board.getComplete(position, func(pos Position) int {return pos.column})
            if completeColumn != nil {
                board.complete = completeColumn
            }
        }
    }
}

func (board Board) getComplete(position Position, f func(Position) int) *[]int {
    var complete []int
    target := f(position)
    for pos, cell := range board.boardMap {
        if f(pos) == target {
            if cell.marked {
                complete = append(complete, cell.value)
            } else {
                return nil
            }
        }
    }
    return &complete
}

func (board Board) score() int {
    total := 0
    for _, cell := range board.boardMap {
        if !cell.marked {
            total += cell.value
        }
    }
    lastMarked := board.markOrder[len(board.markOrder) - 1]
    return total * lastMarked
}

func (board Board) print() {
    for r := 0; r < board.numRows; r++ {
        for c := 0; c < board.numCols; c++ {
            position := Position{r, c}
            cell := board.boardMap[position]
            fmt.Print(*cell)
        }
        fmt.Println()
    }
    fmt.Printf("Is complete = %v \n", *board.complete)
    fmt.Printf("Marked = %v \n", board.markOrder)
}

func main() {
    order, boards := getData()

    completeScores := runToComplete(order, boards)
    // Part 1: 44088
    fmt.Printf("Part 1: %d \n", completeScores[0])
    // Part 2: 23670
    fmt.Printf("Part 2: %d \n", completeScores[len(completeScores) - 1])
}

func runToComplete(order []int, boards []*Board) []int {
    var result []int
    for _, value := range order {
        for _, board := range incomplete(boards) {
            board.mark(value)
            if board.complete != nil {
                result = append(result, board.score()) 
            }
        }
    }
    return result
}

func incomplete(boards []*Board) []*Board {
    var result []*Board
    for _, board := range boards {
        if board.complete == nil {
            result = append(result, board)
        }
    }
    return result
}

func getData() ([]int, []*Board) {
    data, _ := ioutil.ReadFile("data.txt")
    orderBoards := strings.Split(string(data), "\r\n\r\n")
    order, boards := orderBoards[0], orderBoards[1:]
    return parseOrder(order), parseBoards(boards)
}

func parseOrder(order string) []int {
    var result []int
    for _, value := range strings.Split(order, ",") {
        parsed, _ := strconv.Atoi(value)
        result = append(result, parsed)
    }
    return result
}

func parseBoards(boards []string) []*Board {
    var result []*Board
    for _, board := range boards {
        result = append(result, parseBoard(board))
    }
    return result
}

func parseBoard(board string) *Board {
    boardMap := make(map[Position]*Cell)
    rows, numRows, numCols := parseBoardSimple(board)
    for r, row := range rows {
        for c, column := range row {
            positon := Position{r, c}
            value, _ := strconv.Atoi(column)
            cell := Cell{value: value}
            boardMap[positon] = &cell
        }
    }
    return &Board{
        boardMap: boardMap, 
        numRows: numRows, 
        numCols: numCols, 
    }
}

func parseBoardSimple(board string) ([][]string, int, int) {
    var simpleBoard [][]string
    for _, row := range strings.Split(board, "\r\n") {
        simpleBoard = append(simpleBoard, strings.Fields(row))
    }
    return simpleBoard, len(simpleBoard), len(simpleBoard[0])
}
