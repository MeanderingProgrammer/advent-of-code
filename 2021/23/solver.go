package main

import (
	"advent-of-code/commons/go/answers"
	"advent-of-code/commons/go/files"
	"advent-of-code/commons/go/graphs"
	"advent-of-code/commons/go/parsers"
	"advent-of-code/commons/go/utils"
	"fmt"
)

type Type string

const (
	Hallway Type = "."
	Doorway      = "x"
	A            = "A"
	B            = "B"
	C            = "C"
	D            = "D"
)

type Character struct {
	value Type
	moved bool
}

func (character Character) atGoal(vertex graphs.Vertex) bool {
	return character.value == vertex.Value
}

func (character Character) cost() int {
	switch character.value {
	case A:
		return 1
	case B:
		return 10
	case C:
		return 100
	case D:
		return 1000
	default:
		panic("Unkwnown character")
	}
}

type BoardState struct {
	characters map[graphs.Vertex]Character
	cost       int
}

func (state BoardState) Positions() map[graphs.Vertex]interface{} {
	positions := make(map[graphs.Vertex]interface{})
	for position, character := range state.characters {
		positions[position] = character.value
	}
	return positions
}

func (state BoardState) Cost() int {
	return state.cost
}

func (state BoardState) String() *string {
	result := fmt.Sprintf("%v", state.characters)
	return &result
}

func (state BoardState) complete(board Board) bool {
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

func (state BoardState) updateCharacter(start, destination graphs.Vertex) BoardState {
	updated := make(map[graphs.Vertex]Character)
	for position, character := range state.characters {
		if position == start {
			updated[destination] = Character{
				moved: true,
				value: character.value,
			}
		} else {
			updated[position] = character
		}
	}

	distance := utils.Abs(start.Point.X - destination.Point.X)
	distance += start.Point.Y + destination.Point.Y - 2

	return BoardState{
		characters: updated,
		cost:       state.cost + state.characters[start].cost()*distance,
	}
}

type Board struct {
	graph    graphs.Graph
	roomSize int
}

func (board Board) solve(initial BoardState) (int, int) {
	queue, seen, explored := &graphs.Queue{initial}, make(map[string]int), 0

	for queue.Len() > 0 {
		explored++
		state := queue.Next().(BoardState)
		if state.complete(board) {
			return state.cost, explored
		}
		for _, state := range board.legalMoves(state) {
			encodedState := *state.String()
			seenValue, exists := seen[encodedState]
			if !exists || state.Cost() < seenValue {
				seen[encodedState] = state.Cost()
				queue.Add(state)
			}
		}
	}

	panic("Could not find a solution")
}

func (board Board) legalMoves(state BoardState) []BoardState {
	var legalMoves []BoardState
	for start := range state.characters {
		for _, destination := range board.characterLegalMoves(state, start) {
			newState := state.updateCharacter(start, destination)
			legalMoves = append(legalMoves, newState)
		}
	}
	return legalMoves
}

func (board Board) characterLegalMoves(state BoardState, start graphs.Vertex) []graphs.Vertex {
	var reachable []graphs.Vertex
	character := state.characters[start]

	if character.atGoal(start) && character.moved {
		// If we're already at the goal state, then there is nowhere else to go
		return reachable
	}

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
			if board.shouldGo(state, start, destination) {
				reachable = append(reachable, destination)
			}
			toExplore = append(toExplore, destination)
		}
	}

	return reachable
}

func (board Board) shouldGo(state BoardState, start, destination graphs.Vertex) bool {
	value := state.characters[start].value
	if destination.Value == Doorway {
		// Can never stop outside of a room
		return false
	} else if destination.Value == Hallway {
		// Can not move to hallway once we are already in the hallway  must go to a room
		if start.Value == Hallway {
			return false
		}
	} else if value != destination.Value {
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
		if destination.Point.Y != board.roomSize-len(charactersInRoom)+1 {
			return false
		}
	}
	return true
}

func main() {
	answers.Part1(18282, solve(false))
	answers.Part2(50132, solve(true))
}

func solve(extend bool) int {
	board, boardState := getData(extend)
	cost, _ := board.solve(boardState)
	return cost
}

func getData(extend bool) (Board, BoardState) {
	rows := files.ReadLines()

	if extend {
		lastRows := make([]string, 2)
		copy(lastRows, rows[len(rows)-2:])
		rows[len(rows)-2] = "  #D#C#B#A#"
		rows[len(rows)-1] = "  #D#B#A#C#"
		rows = append(rows, lastRows...)
	}

	grid := parsers.ConstructGrid(rows, parsers.Character, "# ")

	characters := make(map[graphs.Vertex]Character)
	for _, point := range grid.Points() {
		value := grid.Get(point)
		if value != "." {
			vertex := graphs.Vertex{Point: point, Value: getType(point)}
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
	state := BoardState{
		characters: characters,
		cost:       0,
	}
	return board, state
}

func getType(position parsers.Point) interface{} {
	result := Hallway
	switch position.X {
	case 3:
		result = A
	case 5:
		result = B
	case 7:
		result = C
	case 9:
		result = D
	}
	if position.Y == 1 && result != Hallway {
		result = Doorway
	}
	return result
}
