package main

import (
    "advent-of-code/commons/go/answers"
    "advent-of-code/commons/go/files"
    "advent-of-code/commons/go/parsers"
    "advent-of-code/commons/go/utils"
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
        if board.pointDetails[characterState.point] == goal {
            inRoom = append(inRoom, characterState.character)
        }
    }
    return inRoom
}

func (boardState *BoardState) updateCharacter(characterIndex int, destination parsers.Point) *BoardState {
    var newStates []CharacterState
    for i, characterState := range boardState.characterStates {
        if i == characterIndex {
            newStates = append(newStates, CharacterState{
                point: destination,
                moved: true,
                character: characterState.character,
            })
        } else {
            newStates = append(newStates, characterState)
        }
    }

    characterState := boardState.characterStates[characterIndex]
    cost := characterState.character.cost()
    start := characterState.point
    distance := utils.Abs(start.X - destination.X) + start.Y + destination.Y - 2

    return &BoardState{
        characterStates: newStates, 
        cost: boardState.cost + cost * distance,
    }
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

    panic("Could not find a solution")
}

func (board *Board) legalMoves(boardState BoardState) []BoardState {
    var legalMoves []BoardState
    for i := range boardState.characterStates {
        for _, point := range board.characterLegalMoves(boardState, i) {
            newState := boardState.updateCharacter(i, point)
            legalMoves = append(legalMoves, *newState)
        }
    }
    return legalMoves
}

func (board *Board) characterLegalMoves(boardState BoardState, i int) []parsers.Point {
    var reachable []parsers.Point
    start := boardState.characterStates[i]
    if start.atGoal(*board) && start.moved {
        // If we're already at the goal state, then there is nowhere else to go
        return reachable
    }

    explored := map[parsers.Point]bool{
        start.point: true,
    }
    toExplore := []parsers.Point{start.point}

    for len(toExplore) > 0 {
        current := toExplore[0]
        toExplore = toExplore[1:]

        for _, destination := range board.graph[current] {
            if explored[destination] || boardState.occupied(destination) {
                // If we've already explored a particular position or that position is occupied
                // then break the chain and do not try to explore from this position
                continue
            }
            explored[destination] = true
            if board.shouldGo(boardState, start, destination) {
                reachable = append(reachable, destination)
            }
            toExplore = append(toExplore, destination)
        }
    }

    return reachable
}

func (board *Board) shouldGo(boardState BoardState, start CharacterState, destination parsers.Point) bool {
    destinationType := board.pointDetails[destination]
    if destinationType == Doorway {
        // Can never stop outside of a room
        return false
    } else if destinationType == Hallway {
        // Can not move to hallway once we are already in the hallway  must go to a room
        if board.pointDetails[start.point] == Hallway {
            return false
        }
    } else {
        // Destination must now be a room
        if start.character.goal() != destinationType {
            // If this room is for another character then we cannot enter
            return false
        } else {
            // Otherwise it is the room for this character, we need to make sure that:
            // 1) Only valid characters are in the room
            // 2) That we go to the correct point in the room, i.e. as far back as possible
            charactersInRoom := boardState.charactersInRoom(board, start.character.goal())
            for _, characterInRoom := range charactersInRoom {
                if characterInRoom != start.character {
                    // At least one character in the room needs to leave
                    return false
                }
            }
            // Must go to back of room
            if destination.Y != board.roomSize - len(charactersInRoom) + 1 {
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
