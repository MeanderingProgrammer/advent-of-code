package main

import (
	"advent-of-code/commons/go/answers"
	"advent-of-code/commons/go/files"
	"advent-of-code/commons/go/graphs"
	"advent-of-code/commons/go/parsers"
	"advent-of-code/commons/go/utils"
	"fmt"
	"math"
)

const PrintStates = false

type Type string

const (
	Hallway Type = "."
	Doorway Type = "x"
	A       Type = "A"
	B       Type = "B"
	C       Type = "C"
	D       Type = "D"
)

func (t Type) distance() int {
	return int(t[0] - 'A')
}

func (t Type) cost() int {
	return int(math.Pow(10, float64(t.distance())))
}

func (t Type) x() int {
	return 3 + t.distance()*2
}

type Character struct {
	value Type
	moved bool
}

func (character Character) atGoal(vertex graphs.Vertex) bool {
	return character.value == vertex.Value
}

type Characters map[graphs.Vertex]Character

type BoardState struct {
	characters Characters
	cost       int
}

func (state BoardState) Cost() int {
	return state.cost
}

func (state BoardState) String() *string {
	result := fmt.Sprintf("%v", state.characters)
	return &result
}

func (state BoardState) complete() bool {
	for vertex, character := range state.characters {
		if !character.atGoal(vertex) {
			return false
		}
	}
	return true
}

func (state BoardState) charactersInRoom(value Type) []Type {
	var inRoom []Type
	for vertex, character := range state.characters {
		if vertex.Value == value {
			inRoom = append(inRoom, character.value)
		}
	}
	return inRoom
}

type Move struct {
	start graphs.Vertex
	end   graphs.Vertex
}

func (state BoardState) move(move Move) BoardState {
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
		cost:       state.cost + cost*distance(move),
	}
}

func distance(move Move) int {
	start, end := move.start.Point, move.end.Point
	distance := utils.Abs(start.X - end.X)
	return distance + start.Y + end.Y - 2
}

func (state BoardState) positions() map[graphs.Vertex]interface{} {
	positions := make(map[graphs.Vertex]interface{})
	for position, character := range state.characters {
		positions[position] = character.value
	}
	return positions
}

type Board struct {
	graph    graphs.Graph
	roomSize int
}

func (board Board) solve(characters Characters) (graphs.State, int) {
	initial := BoardState{
		characters: characters,
		cost:       0,
	}
	done := func(state graphs.State) bool {
		if PrintStates {
			board.graph.Print(state.(BoardState).positions())
		}
		return state.(BoardState).complete()
	}
	nextStates := func(state graphs.State) <-chan graphs.State {
		return board.nextStates(state.(BoardState))
	}
	return board.graph.Bfs(graphs.Search{
		Initial:    initial,
		Done:       done,
		NextStates: nextStates,
	})
}

func (board Board) nextStates(state BoardState) <-chan graphs.State {
	nextStates := make(chan graphs.State)
	go func() {
		defer close(nextStates)
		for start, character := range state.characters {
			// Check that the character hasn't already been moved to their goal
			if !character.atGoal(start) || !character.moved {
				for _, move := range board.characterMoves(state, start) {
					nextStates <- state.move(move)
				}
			}
		}
	}()
	return nextStates
}

func (board Board) characterMoves(state BoardState, start graphs.Vertex) []Move {
	var moves []Move
	explored := map[graphs.Vertex]bool{start: true}
	toExplore := []graphs.Vertex{start}

	for len(toExplore) > 0 {
		current := toExplore[0]
		toExplore = toExplore[1:]

		for _, destination := range board.graph.Neighbors(current) {
			_, occupied := state.characters[destination]
			if explored[destination] || occupied {
				// If we've already explored a particular position or that position is occupied
				// then break the chain and do not try to explore from this position
				continue
			}
			explored[destination] = true
			move := Move{start: start, end: destination}
			if board.shouldGo(state, move) {
				moves = append(moves, move)
			}
			toExplore = append(toExplore, destination)
		}
	}

	return moves
}

func (board Board) shouldGo(state BoardState, move Move) bool {
	value := state.characters[move.start].value
	if move.end.Value == Doorway {
		// Can never stop outside of a room
		return false
	} else if move.end.Value == Hallway {
		// Can not move to hallway once we are already in the hallway must go to a room
		if move.start.Value == Hallway {
			return false
		}
		// Here we detect "deadlock", which occurs when we put our character in the Hallway
		// and they block a character from reaching their room who is in turn blocking them
		for _, point := range pathToGoal(move.end, value) {
			onPath, exists := state.characters[point]
			if !exists {
				continue
			}
			deadlock := contains(pathToGoal(point, onPath.value), move.end)
			if deadlock {
				return false
			}
		}
	} else if value != move.end.Value {
		// If this room is for another character then we cannot enter
		return false
	} else {
		// Otherwise it is the room for this character, we need to make sure that:
		// 1) Only valid characters are in the room
		// 2) That we go to the correct point in the room, i.e. as far back as possible
		charactersInRoom := state.charactersInRoom(value)
		for _, characterInRoom := range charactersInRoom {
			if characterInRoom != value {
				// At least one character in the room needs to leave
				return false
			}
		}
		// Must go to back of room
		if move.end.Point.Y != board.roomSize-len(charactersInRoom)+1 {
			return false
		}
	}
	return true
}

func pathToGoal(location graphs.Vertex, value Type) []graphs.Vertex {
	var result []graphs.Vertex
	x1, x2 := location.Point.X, value.x()
	for i := utils.Min(x1, x2) + 1; i < utils.Max(x1, x2); i++ {
		vertex := graphs.Vertex{
			Point: parsers.Point{X: i, Y: 1},
			Value: Hallway,
		}
		result = append(result, vertex)
	}
	return result
}

func contains(path []graphs.Vertex, target graphs.Vertex) bool {
	for _, vertex := range path {
		if vertex == target {
			return true
		}
	}
	return false
}

func main() {
	answers.Part1(18282, solve(false))
	answers.Part2(50132, solve(true))
}

func solve(extend bool) int {
	board, characters := getData(extend)
	endState, _ := board.solve(characters)
	return endState.(BoardState).cost
}

func getData(extend bool) (Board, Characters) {
	rows := files.ReadLines()
	if extend {
		lastRows := make([]string, 2)
		copy(lastRows, rows[len(rows)-2:])
		rows[len(rows)-2] = "  #D#C#B#A#"
		rows[len(rows)-1] = "  #D#B#A#C#"
		rows = append(rows, lastRows...)
	}

	grid := parsers.ConstructGrid(rows, parsers.Character, "# ")

	characters := make(Characters)
	for _, point := range grid.Points() {
		value := grid.Get(point)
		if value != "." {
			vertex := graphs.ConstructVertex(point, grid, getType)
			characters[vertex] = Character{
				value: Type(value),
				moved: false,
			}
		}
	}

	board := Board{
		graph:    graphs.ConstructGraph(grid, getType),
		roomSize: grid.Height - 2,
	}
	return board, characters
}

func getType(position parsers.Point, value string) interface{} {
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
}
