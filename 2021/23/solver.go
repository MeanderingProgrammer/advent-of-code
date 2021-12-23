package main

import(
    "fmt"
    "io/ioutil"
    "strings"
)

type LocationType int
const (
	Hallway LocationType = iota
    Doorway
	AGoal
	BGoal
	CGoal
    DGoal
)

type CharacterType int
const (
	A CharacterType = iota
    B
	C
    D
)

func (characterType CharacterType) cost() int {
    switch characterType {
    case A: return 1
    case B: return 10
    case C: return 100
    case D: return 1000
    default: return 0
    }
}

func (characterType CharacterType) goal() LocationType {
    switch characterType {
    case A: return AGoal
    case B: return BGoal
    case C: return CGoal
    case D: return DGoal
    default: return 0
    }
}

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

type PositionCost map[Position]int

type Character struct {
    characterType CharacterType
    position Position
}

func (character Character) legalMoves(board Board, state State) PositionCost {
    fmt.Println(character)
    positionCost := character.reachable(board, state)
    var toDelete []Position
    for position := range positionCost {
        locationType, shouldDelete := board[position], false
        if locationType == Doorway {
            // Can never stop outside of a room
            shouldDelete = true
        } else if locationType == Hallway {
            // Can not move once we are already in the hallway
            // must go to a reom
            if board[character.position] == Hallway {
                shouldDelete = true
            }
        } else {
            // Destination must now be a goal, i.e. a room
            if character.characterType.goal() != locationType {
                // If this is for another character then we cannot
                // enter their reoom
                shouldDelete = true
            } else {
                // Otherwise it is the room for this character, we need
                // to make sure that only valid characters are in the room
                for _, inRoom := range state.charactersInRoom(board, character.characterType.goal()) {
                    if inRoom != character.characterType {
                        shouldDelete = true
                    }
                }
            }
        }
        if shouldDelete {
            toDelete = append(toDelete, position)
        }
    }
    for _, position := range toDelete {
        delete(positionCost, position)
    }
    return positionCost
}

func (character Character) reachable(board Board, state State) PositionCost {
    positionCost, toExplore := make(PositionCost), []Position{character.position}
    positionCost[character.position] = 0

    for len(toExplore) > 0 {
        position, baseCost := toExplore[0], positionCost[toExplore[0]]        
        toExplore = toExplore[1:]
        for _, adjacent := range position.adjacent() {
            _, explored := positionCost[adjacent]
            if explored {
                continue
            }
            _, onBoard := board[adjacent]
            if !onBoard {
                continue
            }
            _, occupied := state.positions[adjacent]
            if occupied {
                continue
            }
            positionCost[adjacent] = baseCost + character.characterType.cost()
            toExplore = append(toExplore, adjacent)
        }
    }

    delete(positionCost, character.position)
    return positionCost
}

type Board map[Position]LocationType

type Characters []Character

func (characters Characters) shuffle(board Board) {
    state := characters.state()
    characters.legalMoves(board, state)
}

type State struct {
    positions map[Position]Character
    cost int
}

func (state State) charactersInRoom(board Board, goal LocationType) []CharacterType {
    var inRoom []CharacterType
    for position, locationType := range board {
        if goal != locationType {
            continue
        }
        character, present := state.positions[position]
        if !present {
            continue
        }
        inRoom = append(inRoom, character.characterType)
    }
    return inRoom
}

func (characters Characters) state() State {
    state := make(map[Position]Character)
    for _, character := range characters {
        state[character.position] = character
    }
    return State{state, 0}
}

func (characters Characters) legalMoves(board Board, state State) {
    fmt.Println(state)
    for _, character := range characters {
        options := character.legalMoves(board, state)
        fmt.Println(options)
    }
}

func main() {
    board, characters := getData()
    fmt.Println(board)
    fmt.Println(characters)
    // 18342 too high
    characters.shuffle(board)
}

func getData() (Board, Characters) {
    data, _ := ioutil.ReadFile("sample.txt")
    rows := strings.Split(string(data), "\r\n")
    var characters []Character
    board := make(Board)
    for y, row := range rows {
        for x, value := range row {
            if value != '#' && value != ' ' {
                position := Position{x, y}
                board[position] = getLocationType(position)
                if value != '.' {
                    characters = append(characters,  getCharacter(position, value))
                }
            }
        }
    }
    return board, characters
}

func getCharacter(position Position, value rune) Character {
    chacter := Character{position: position}
    if value == 'A' {
        chacter.characterType = A
    } else if value == 'B' {
        chacter.characterType = B
    } else if value == 'C' {
        chacter.characterType = C
    } else if value == 'D' {
        chacter.characterType = D
    }
    return chacter
}

func getLocationType(position Position) LocationType {
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
    }
    fmt.Println("UNEXPECTED")
    return Hallway
}
