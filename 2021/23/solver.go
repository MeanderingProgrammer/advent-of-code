package main

import (
    "advent-of-code/commons/go/answers"
    "advent-of-code/commons/go/files"
    "advent-of-code/commons/go/parsers"
	"container/heap"
	"fmt"
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

type Character int
const (
	A Character = iota
    B
	C
    D
)

type CharacterState struct {
    point parsers.Point
    moved bool
    character Character
}

func (characterState CharacterState) atGoal(board Board) bool {
    current := board.pointDetails[characterState.point]
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
    pointDetails map[parsers.Point]Location
    graph map[parsers.Point][]parsers.Point
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

func (boardState *BoardState) occupied(point parsers.Point) bool {
    for _, characterState := range boardState.characterStates {
        if characterState.point == point {
            return true
        }
    }
    return false
}

func (boardState *BoardState) charactersInRoom(board *Board, goal Location) []Character {
    var inRoom []Character
    for _, characterState := range boardState.characterStates {
        location := board.pointDetails[characterState.point]
        if location == goal {
            inRoom = append(inRoom, characterState.character)
        }
    }
    return inRoom
}

func (boardState *BoardState) update(characterIndex int, point parsers.Point, moves int) *BoardState {
    var newStates []CharacterState
    newCost := boardState.cost
    for i, characterState := range boardState.characterStates {
        if i == characterIndex {
            character := characterState.character
            newCost += (character.cost() * moves)
            newCharacterState := CharacterState{point, true, character}
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

func (board *Board) solve(initial BoardState) (int, int) {
    queue, seen, explored := &Queue{initial}, make(map[string]bool), 0

    for queue.Len() > 0 {
        explored++
        currentState := heap.Pop(queue).(BoardState)
        if currentState.complete(*board) {
            return currentState.cost, explored
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

    return -1, explored
}

func (board *Board) legalMoves(boardState BoardState) []BoardState {
    var legalMoves []BoardState
    for i := range boardState.characterStates {
        for point, moves := range board.characterLegalMoves(boardState, i) {
            newState := boardState.update(i, point, moves)
            legalMoves = append(legalMoves, *newState)
        }
    }
    return legalMoves
}

type PointMoves map[parsers.Point]int

func (board *Board) characterLegalMoves(boardState BoardState, i int) PointMoves {
    characterState := boardState.characterStates[i]
    if characterState.atGoal(*board) && characterState.moved {
        // If we're already at the goal state, then there is nowhere else to go
        return nil
    }

    reachable := board.reachable(boardState, characterState.point)

    var toDelete []parsers.Point
    for destination := range reachable {
        destinationType, shouldDelete := board.pointDetails[destination], false
        if destination == characterState.point {
            // Remove moving nowhere as an option
            shouldDelete = true
        } else if destinationType == Doorway {
            // Can never stop outside of a room
            shouldDelete = true
        } else if destinationType == Hallway {
            // Can not move to hallway once we are already in the hallway  must go to a room
            if board.pointDetails[characterState.point] == Hallway {
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
                // 2) That we go to the correct point in the room, i.e. as far back as possible
                charactersInRoom, allValid := boardState.charactersInRoom(board, characterState.character.goal()), true
                for _, characterInRoom := range charactersInRoom {
                    if characterInRoom != characterState.character {
                        allValid = false
                    }
                }
                if allValid {
                    // Must go to back of room
                    if destination.Y != board.roomSize - len(charactersInRoom) + 1 {
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

    for _, point := range toDelete {
        delete(reachable, point)
    }

    return reachable
}

func (board *Board) reachable(boardState BoardState, point parsers.Point) PointMoves {
    pointMoves, toExplore := PointMoves{point: 0}, []parsers.Point{point}

    for len(toExplore) > 0 {
        currentPoint, currentMoves := toExplore[0], pointMoves[toExplore[0]]        
        toExplore = toExplore[1:]

        for _, adjacent := range board.graph[currentPoint] {
            _, explored := pointMoves[adjacent]
            if explored {
                continue
            }
            if boardState.occupied(adjacent) {
                continue
            }
            pointMoves[adjacent] = currentMoves + 1
            toExplore = append(toExplore, adjacent)
        }
    }

    return pointMoves
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
        length := len(rows)
        lastRows := []string{
            rows[length - 2],
            rows[length - 1],
        }
        rows[length - 2] = "  #D#C#B#A#"
        rows[length - 1] = "  #D#B#A#C#"
        rows = append(rows, lastRows...)
    }

    pointDetails := make(map[parsers.Point]Location)
    var characterStates []CharacterState
    
    for y, row := range rows {
        for x, value := range row {
            if value == '#' || value == ' ' {
                continue
            }
            point := parsers.Point{X: x, Y: y}
            pointDetails[point] = location(point)
            if value != '.' {
                characterStates = append(characterStates, CharacterState{point, false, character(value)})
            }
        }
    }

    return Board{
        pointDetails: pointDetails, 
        graph: graph(pointDetails), 
        roomSize: len(rows) - 3,
    }, BoardState{
        characterStates: characterStates, 
        cost: 0,
    }
}

func location(point parsers.Point) Location {
    goalMapping := map[int]Location{
        3: AGoal,
        5: BGoal,
        7: CGoal,
        9: DGoal,
    }
    goal, exists := goalMapping[point.X]

    if point.Y == 1 {
        if exists {
            return Doorway
        } else {
            return Hallway
        }
    } else {
        if exists {
            return goal
        } else {
            panic(fmt.Sprintf("Can't figure out location for: (%v)", point))
        }
    }
}

func character(value rune) Character {
    characterMapping := map[rune]Character{
        'A': A,
        'B': B,
        'C': C,
        'D': D,
    }
    character, exists := characterMapping[value]
    if !exists {
        panic(fmt.Sprintf("Can't figure out character for: %v", value))
    }
    return character
}

func graph(pointDetails map[parsers.Point]Location) map[parsers.Point][]parsers.Point {
    result := make(map[parsers.Point][]parsers.Point)
    for point := range pointDetails {
        var connected []parsers.Point
        for _, adjacent := range point.Adjacent(false) {
            _, exists := pointDetails[adjacent]
            if exists {
                connected = append(connected, adjacent)
            }
        }
        result[point] = connected
    }
    return result
}
