package main

import (
	"advent-of-code/commons/go/answers"
	"advent-of-code/commons/go/files"
	"advent-of-code/commons/go/graphs"
	"advent-of-code/commons/go/parsers"
	"advent-of-code/commons/go/utils"
	"fmt"
)

const (
	Hallway = "HALL"
	Doorway = "DOOR"
	A       = "A"
	B       = "B"
	C       = "C"
	D       = "D"
)

func getType(position parsers.Point) string {
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

type CharacterState struct {
	character string
	moved     bool
}

func (characterState CharacterState) atGoal(position parsers.Point) bool {
	return characterState.character == getType(position)
}

func (characterState CharacterState) cost() int {
	switch characterState.character {
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
	characterStates map[parsers.Point]CharacterState
	cost            int
}

func (state BoardState) Cost() int {
	return state.cost
}

func (state BoardState) String() *string {
	result := fmt.Sprintf("%v", state)
	return &result
}

func (state BoardState) complete(board Board) bool {
	for position, characterState := range state.characterStates {
		if getType(position) != characterState.character {
			return false
		}
	}
	return true
}

func (state BoardState) charactersInRoom(character string) []string {
	var inRoom []string
	for position, characterState := range state.characterStates {
		if getType(position) == character {
			inRoom = append(inRoom, characterState.character)
		}
	}
	return inRoom
}

func (state BoardState) updateCharacter(start, destination parsers.Point) BoardState {
	newStates := make(map[parsers.Point]CharacterState)
	for position, characterState := range state.characterStates {
		if position == start {
			newStates[destination] = CharacterState{
				moved:     true,
				character: characterState.character,
			}
		} else {
			newStates[position] = characterState
		}
	}

	characterState := state.characterStates[start]
	distance := utils.Abs(start.X-destination.X) + start.Y + destination.Y - 2

	return BoardState{
		characterStates: newStates,
		cost:            state.cost + characterState.cost()*distance,
	}
}

type Board struct {
	graph    graphs.Graph
	roomSize int
}

func (board Board) solve(initial BoardState) (int, int) {
	queue, seen, explored := &graphs.Queue{initial}, make(map[string]bool), 0

	for queue.Len() > 0 {
		explored++
		state := queue.Next().(BoardState)
		if state.complete(board) {
			return state.cost, explored
		}
		for _, state := range board.legalMoves(state) {
			asString := *state.String()
			if !seen[asString] {
				seen[asString] = true
				queue.Add(state)
			}
		}
	}

	panic("Could not find a solution")
}

func (board Board) legalMoves(state BoardState) []BoardState {
	var legalMoves []BoardState
	for start := range state.characterStates {
		for _, destination := range board.characterLegalMoves(state, start) {
			newState := state.updateCharacter(start, destination)
			legalMoves = append(legalMoves, newState)
		}
	}
	return legalMoves
}

func (board Board) characterLegalMoves(state BoardState, start parsers.Point) []parsers.Point {
	var reachable []parsers.Point
	characterState := state.characterStates[start]

	if characterState.atGoal(start) && characterState.moved {
		// If we're already at the goal state, then there is nowhere else to go
		return reachable
	}

	explored := map[parsers.Point]bool{start: true}
	toExplore := []parsers.Point{start}

	for len(toExplore) > 0 {
		current := toExplore[0]
		toExplore = toExplore[1:]

		for _, destination := range board.graph[current] {
			_, occupied := state.characterStates[destination]
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

func (board Board) shouldGo(state BoardState, start, destination parsers.Point) bool {
	startType, destinationType := getType(start), getType(destination)

	if destinationType == Doorway {
		// Can never stop outside of a room
		return false
	} else if destinationType == Hallway {
		// Can not move to hallway once we are already in the hallway  must go to a room
		if startType == Hallway {
			return false
		}
	} else {
		character := state.characterStates[start].character
		// Destination must now be a room
		if character != destinationType {
			// If this room is for another character then we cannot enter
			return false
		} else {
			// Otherwise it is the room for this character, we need to make sure that:
			// 1) Only valid characters are in the room
			// 2) That we go to the correct point in the room, i.e. as far back as possible
			charactersInRoom := state.charactersInRoom(character)
			for _, characterInRoom := range charactersInRoom {
				if characterInRoom != character {
					// At least one character in the room needs to leave
					return false
				}
			}
			// Must go to back of room
			if destination.Y != board.roomSize-len(charactersInRoom)+1 {
				return false
			}
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
	cost, explored := board.solve(boardState)
	fmt.Println(explored)
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

	characterStates := make(map[parsers.Point]CharacterState)
	for _, point := range grid.Points() {
		value := grid.Get(point)
		if value != "." {
			characterStates[point] = CharacterState{
				character: value,
				moved:     false,
			}
		}
	}

	board := Board{
		graph:    graphs.ConstructGraph(grid),
		roomSize: grid.Height - 2,
	}
	state := BoardState{
		characterStates: characterStates,
		cost:            0,
	}
	return board, state
}
