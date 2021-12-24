package main

import (
	"container/heap"
	"fmt"
	"io/ioutil"
	"strings"
)

type Location int
const (
	Hallway Location = iota
    Doorway
	AGoal
	BGoal
	CGoal
    DGoal
)

type Position struct {
    x int
    y int
}

func (position Position) adjacent() []Position {
    return []Position{
        {x: position.x-1, y: position.y},
        {x: position.x+1, y: position.y},
        {x: position.x, y: position.y-1},
        {x: position.x, y: position.y+1},
    }
}

type Character int
const (
	A Character = iota
    B
	C
    D
)

type CharacterState struct {
    position Position
    moved bool
    character Character
}

func (characterState CharacterState) atGoal(board Board) bool {
    current := board.positionDetails[characterState.position]
    return current == characterState.character.goal()
}

func (character Character) cost() int {
    switch character {
    case A: return 1
    case B: return 10
    case C: return 100
    case D: return 1000
    default: panic(fmt.Sprintf("Unknown character type: %d", character))
    }
}

func (character Character) goal() Location {
    switch character {
    case A: return AGoal
    case B: return BGoal
    case C: return CGoal
    case D: return DGoal
    default: panic(fmt.Sprintf("Unknown character type: %d", character))
    }
}

type Board struct {
    positionDetails map[Position]Location
    graph map[Position][]Position
    roomSize int
}

type BoardState struct {
    characterStates []CharacterState
    cost int
}

func (boardState *BoardState) String() *string {
    result := fmt.Sprintf("%v", boardState)
    return &result
}

func (boardState *BoardState) complete(board Board) bool {
    for _, characterState := range boardState.characterStates {
        if !characterState.atGoal(board) {
            return false
        }
    }
    return true
}

func (boardState *BoardState) occupied(position Position) bool {
    for _, characterState := range boardState.characterStates {
        if characterState.position == position {
            return true
        }
    }
    return false
}

func (boardState *BoardState) charactersInRoom(board *Board, goal Location) []Character {
    var inRoom []Character
    for _, characterState := range boardState.characterStates {
        location := board.positionDetails[characterState.position]
        if location == goal {
            inRoom = append(inRoom, characterState.character)
        }
    }
    return inRoom
}

func (boardState *BoardState) update(characterIndex int, position Position, moves int) *BoardState {
    var newStates []CharacterState
    newCost := boardState.cost
    for i, characterState := range boardState.characterStates {
        if i == characterIndex {
            character := characterState.character
            newCost += (character.cost() * moves)
            newCharacterState := CharacterState{position, true, character}
            newStates = append(newStates, newCharacterState)
        } else {
            newStates = append(newStates, characterState)
        }
    }
    result := BoardState{newStates, newCost}
    return &result
}

type Queue []BoardState

func (q Queue) Len() int {
    return len(q)
}

func (q Queue) Less(i, j int) bool {
    return q[i].cost < q[j].cost
}

func (q Queue) Swap(i, j int) { 
    q[i], q[j] = q[j], q[i] 
}

func (q *Queue) Pop() interface{} {
    length := len(*q)
    result := (*q)[length -1]
	*q = (*q)[:length - 1]
	return result
}

func (q *Queue) Push(state interface{}) {
	*q = append(*q, state.(BoardState))
}

func (board *Board) solve(initial BoardState) int {
    queue, seen := &Queue{initial}, make(map[string]bool)

    for queue.Len() > 0 {
        currentState := heap.Pop(queue).(BoardState)
        if currentState.complete(*board) {
            return currentState.cost
        }
        legalMoves := board.legalMoves(currentState)
        for _, state := range legalMoves {
            asString := *state.String()
            if !seen[asString] {
                seen[asString] = true
                heap.Push(queue, state)
            }
        }
    }

    return -1
}

func (board *Board) legalMoves(boardState BoardState) []BoardState {
    var legalMoves []BoardState
    for i := range boardState.characterStates {
        positionMoves := board.characterLegalMoves(boardState, i)
        for position, moves := range positionMoves {
            newState := boardState.update(i, position, moves)
            legalMoves = append(legalMoves, *newState)
        }
    }
    return legalMoves
}

type PositionMoves map[Position]int

func (board *Board) characterLegalMoves(boardState BoardState, i int) PositionMoves {
    characterState := boardState.characterStates[i]
    if characterState.atGoal(*board) && characterState.moved {
        // If we're already at the goal state, then there is nowhere else to go
        return nil
    }

    reachable := board.reachable(boardState, characterState.position)

    var toDelete []Position
    for destination := range reachable {
        destinationType, shouldDelete := board.positionDetails[destination], false
        if destination == characterState.position {
            // Remove moving nowhere as an option
            shouldDelete = true
        } else if destinationType == Doorway {
            // Can never stop outside of a room
            shouldDelete = true
        } else if destinationType == Hallway {
            // Can not move to hallway once we are already in the hallway  must go to a room
            if board.positionDetails[characterState.position] == Hallway {
                shouldDelete = true
            }
        } else {
            // Destination must now be a room
            if characterState.character.goal() != destinationType {
                // If this room is for another character then we cannot enter
                shouldDelete = true
            } else {
                // Otherwise it is the room for this character, we need to make sure that:
                // 1) Only valid characters are in the room
                // 2) That we go to the correct position in the room, i.e. as far back as possible
                charactersInRoom, allValid := boardState.charactersInRoom(board, characterState.character.goal()), true
                for _, characterInRoom := range charactersInRoom {
                    if characterInRoom != characterState.character {
                        allValid = false
                    }
                }
                if allValid {
                    // Must go to back of room
                    if destination.y != board.roomSize - len(charactersInRoom) + 1 {
                        shouldDelete = true
                    }
                } else {
                    // At least one character in the room needs to leave
                    shouldDelete = true
                }
            }
        }
        if shouldDelete {
            toDelete = append(toDelete, destination)
        }
    }

    for _, position := range toDelete {
        delete(reachable, position)
    }

    return reachable
}

func (board *Board) reachable(boardState BoardState, position Position) PositionMoves {
    positionMoves, toExplore := PositionMoves{position: 0}, []Position{position}

    for len(toExplore) > 0 {
        currentPosition, currentMoves := toExplore[0], positionMoves[toExplore[0]]        
        toExplore = toExplore[1:]

        for _, adjacent := range board.graph[currentPosition] {
            _, explored := positionMoves[adjacent]
            if explored {
                continue
            }
            if boardState.occupied(adjacent) {
                continue
            }
            positionMoves[adjacent] = currentMoves + 1
            toExplore = append(toExplore, adjacent)
        }
    }

    return positionMoves
}

func main() {
    fmt.Printf("Part 1 = %d \n", solve(false))
    fmt.Printf("Part 2 = %d \n", solve(true))
}

func solve(extend bool) int {
    board, boardState := getData(extend)
    return board.solve(boardState)
}

func getData(extend bool) (Board, BoardState) {
    data, _ := ioutil.ReadFile("data.txt")
    rows := strings.Split(string(data), "\r\n")

    if extend {
        length := len(rows)
        lastRows := []string{
            rows[length - 2],
            rows[length - 1],
        }
        rows[length - 2] = "  #D#C#B#A#"
        rows[length - 1] = "  #D#B#A#C#"
        rows = append(rows, lastRows...)
    }

    positionDetails := make(map[Position]Location)
    var characterStates []CharacterState
    
    for y, row := range rows {
        for x, value := range row {
            if value == '#' || value == ' ' {
                continue
            }
            position := Position{x, y}
            positionDetails[position] = location(position)
            if value != '.' {
                characterStates = append(characterStates, CharacterState{position, false, character(value)})
            }
        }
    }

    return Board{
        positionDetails: positionDetails, 
        graph: graph(positionDetails), 
        roomSize: len(rows) - 3,
    }, BoardState{
        characterStates: characterStates, 
        cost: 0,
    }
}

func location(position Position) Location {
    x, y := position.x, position.y
    if y == 1 {
        if x == 3 || x == 5 || x == 7 || x == 9 {
            return Doorway
        } else {
            return Hallway
        }
    } else if x == 3 {
        return AGoal
    } else if x == 5 {
        return BGoal
    } else if x == 7 {
        return CGoal
    } else if x == 9 {
        return DGoal
    } else {
        panic(fmt.Sprintf("Can't figure out location for: (%d, %d)", x, y))
    }
}

func character(value rune) Character {
    if value == 'A' {
        return A
    } else if value == 'B' {
        return B
    } else if value == 'C' {
        return C
    } else if value == 'D' {
        return D
    } else {
        panic(fmt.Sprintf("Can't figure out character for: %v", value))
    }
}

func graph(positionDetails map[Position]Location) map[Position][]Position {
    result := make(map[Position][]Position)
    for position := range positionDetails {
        var connected []Position
        for _, adjacent := range position.adjacent() {
            _, exists := positionDetails[adjacent]
            if exists {
                connected = append(connected, adjacent)
            }
        }
        result[position] = connected
    }
    return result
}
