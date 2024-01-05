package main

import (
	"advent-of-code/commons/go/answer"
	"advent-of-code/commons/go/file"
	"advent-of-code/commons/go/graph"
	"advent-of-code/commons/go/parser"
	"advent-of-code/commons/go/point"
	"advent-of-code/commons/go/util"
	"fmt"
	"hash/fnv"
	"math"
)

type Value string

const (
	Hallway Value = "."
	Doorway Value = "x"
	A       Value = "A"
	B       Value = "B"
	C       Value = "C"
	D       Value = "D"
)

func (v Value) distance() int {
	return int(v[0] - 'A')
}

func (v Value) cost() int {
	return int(math.Pow(10, float64(v.distance())))
}

func (v Value) x() int {
	return 3 + v.distance()*2
}

func (v Value) pathToGoal(start point.Point) []point.Point {
	result := []point.Point{}
	x1, x2 := start.X, v.x()
	for i := util.Min(x1, x2) + 1; i < util.Max(x1, x2); i++ {
		result = append(result, point.Point{X: i, Y: 1})
	}
	return result
}

type Character struct {
	value Value
	moved bool
}

func (character Character) atGoal(p point.Point) bool {
	return character.value.x() == p.X
}

type Characters map[point.Point]Character

type BoardState struct {
	characters Characters
	cost       int
}

func (state BoardState) Cost() int {
	return state.cost
}

func (state BoardState) Hash() uint64 {
	h := fnv.New64()
	// for point, character := range state.characters {
	// 	h.Write([]byte(util.ToString(point.X)))
	// 	h.Write([]byte(util.ToString(point.Y)))
	// 	h.Write([]byte(character.value))
	// 	if character.moved {
	// 		h.Write([]byte{1})
	// 	} else {
	// 		h.Write([]byte{0})
	// 	}
	// }
	h.Write([]byte(fmt.Sprintf("%v", state.characters)))
	return h.Sum64()
}

func (state BoardState) complete() bool {
	for point, character := range state.characters {
		if !character.atGoal(point) {
			return false
		}
	}
	return true
}

func (state BoardState) charactersInRoom(value Value) []Value {
	var inRoom []Value
	for point, character := range state.characters {
		if point.X == value.x() {
			inRoom = append(inRoom, character.value)
		}
	}
	return inRoom
}

func (state BoardState) apply(move Move) BoardState {
	updated, cost := make(Characters), 0
	for position, character := range state.characters {
		if position != move.start {
			updated[position] = character
		} else {
			updated[move.end] = Character{
				moved: true,
				value: character.value,
			}
			cost = character.value.cost()
		}
	}
	return BoardState{
		characters: updated,
		cost:       state.cost + cost*move.distance(),
	}
}

type Move struct {
	start point.Point
	end   point.Point
}

func (move Move) distance() int {
	start, end := move.start, move.end
	distance := util.Abs(start.X - end.X)
	return distance + start.Y + end.Y - 2
}

type Board struct {
	graph    graph.Graph[point.Point, Value]
	roomSize int
}

func (board Board) solve(characters Characters) BoardState {
	result := graph.Search[BoardState]{
		Initial: BoardState{
			characters: characters,
			cost:       0,
		},
		Done: func(state BoardState) bool {
			return state.complete()
		},
		NextStates: func(state BoardState) []BoardState {
			return board.nextStates(state)
		},
		FirstOnly: true,
	}.Bfs()
	return result.Completed[0]
}

func (board Board) nextStates(state BoardState) []BoardState {
	nextStates := []BoardState{}
	for start, character := range state.characters {
		if !character.atGoal(start) || !character.moved {
			for _, move := range board.moves(state, start) {
				nextStates = append(nextStates, state.apply(move))
			}
		}
	}
	return nextStates
}

func (board Board) moves(state BoardState, start point.Point) []Move {
	moves := []Move{}
	explored := map[point.Point]bool{start: true}
	toExplore := []point.Point{start}
	for len(toExplore) > 0 {
		current := toExplore[0]
		toExplore = toExplore[1:]
		for _, destination := range board.graph.Neighbors(current) {
			_, ok := state.characters[destination]
			if explored[destination] || ok {
				// If we've already explored a particular position or that position is occupied
				// then break the chain and do not try to explore from this position
				continue
			}
			explored[destination] = true
			move := Move{start: start, end: destination}
			if board.valid(state, move) {
				moves = append(moves, move)
			}
			toExplore = append(toExplore, destination)
		}
	}
	return moves
}

func (board Board) valid(state BoardState, move Move) bool {
	currentValue := state.characters[move.start].value
	endValue := board.graph.Value(move.end)
	if endValue == Doorway {
		// Can never stop outside of a room
		return false
	} else if endValue == Hallway {
		// Can not move to hallway once we are already in the hallway must go to a room
		if board.graph.Value(move.start) == Hallway {
			return false
		}
		// Here we detect "deadlock", which occurs when we put our character in the Hallway
		// and this blocks a character from reaching their room who is in turn blocking us
		for _, point := range currentValue.pathToGoal(move.end) {
			characterOnPath, ok := state.characters[point]
			if !ok {
				continue
			}
			characterOnPathGoalPath := characterOnPath.value.pathToGoal(point)
			if util.Contains(characterOnPathGoalPath, move.end) {
				return false
			}
		}
	} else if currentValue != endValue {
		// If this room is for another character then we cannot enter
		return false
	} else {
		// Otherwise it is the room for this character, we need to make sure that:
		// 1) Only valid characters are in the room
		// 2) That we go to the correct point in the room, i.e. as far back as possible
		charactersInRoom := state.charactersInRoom(currentValue)
		for _, characterInRoom := range charactersInRoom {
			if characterInRoom != currentValue {
				// At least one character in the room needs to leave
				return false
			}
		}
		// Must go to back of room
		if move.end.Y != board.roomSize-len(charactersInRoom)+1 {
			return false
		}
	}
	return true
}

func main() {
	answer.Timer(solution)
}

func solution() {
	answer.Part1(18282, solve(false))
	answer.Part2(50132, solve(true))
}

func solve(extend bool) int {
	rows := getRows(extend)
	board := getBoard(rows)
	characters := getCharacters(rows)
	endState := board.solve(characters)
	return endState.cost
}

func getRows(extend bool) []string {
	rows := file.ReadLines()
	if extend {
		lastRows := make([]string, 2)
		copy(lastRows, rows[len(rows)-2:])
		rows[len(rows)-2] = "  #D#C#B#A#"
		rows[len(rows)-1] = "  #D#B#A#C#"
		rows = append(rows, lastRows...)
	}
	return rows
}

func getBoard(rows []string) Board {
	grid := parser.GridMaker[Value]{
		Rows:     rows,
		Splitter: parser.Character,
		Ignore:   "# ",
		Transformer: func(position point.Point, value string) Value {
			result := Hallway
			switch position.X {
			case A.x():
				result = A
			case B.x():
				result = B
			case C.x():
				result = C
			case D.x():
				result = D
			}
			if position.Y == 1 && result != Hallway {
				result = Doorway
			}
			return result
		},
	}.Construct()
	return Board{
		graph:    graph.ConstructGraph(grid),
		roomSize: grid.Height - 2,
	}
}

func getCharacters(rows []string) Characters {
	grid := parser.GridMaker[Value]{
		Rows:     rows,
		Splitter: parser.Character,
		Ignore:   ".# ",
		Transformer: func(position point.Point, value string) Value {
			return Value(value)
		},
	}.Construct()
	characters := make(Characters)
	for _, p := range grid.Points() {
		characters[p] = Character{
			value: grid.Get(p),
			moved: false,
		}
	}
	return characters
}
