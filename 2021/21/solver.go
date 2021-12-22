package main

import(
    "fmt"
    "io/ioutil"
    "strconv"
    "strings"
)

type Player struct {
    position int
    score int
    moves int
}

func (player Player) move(amount int) Player {
    newPosition := player.position + amount
    newPosition = ((newPosition - 1) % 10) + 1
    return Player{
        position: newPosition,
        score: player.score + newPosition,
        moves: player.moves + 1,
    }
}

type GameState struct {
    p1 Player
    p2 Player
}

type GameStateFrequency map[GameState]int

func (gameFrequencies GameStateFrequency) total() int {
    result := 0
    for _, frequency := range gameFrequencies {
        result += frequency
    }
    return result
}

type PlayerState struct {
    player Player
    frequency int
}

type Game struct {
    target int
    stateUpdater func(Player)[](PlayerState)
}

func (game Game) play(p1 Player, p2 Player) GameStateFrequency {
    isP1 := true
    p1Wins, p2Wins := make(GameStateFrequency), make(GameStateFrequency)

    states := make(GameStateFrequency)
    states[GameState{
        p1: p1,
        p2: p2,
    }]++

    for len(states) > 0 {
        if isP1 {
            states = game.step(states, p1Wins)
        } else {
            states = game.step(states, p2Wins)
        }
        isP1 = !isP1
    }

    if p1Wins.total() > p2Wins.total() {
        return p1Wins
    } else {
        return p2Wins
    }
}

func (game Game) step(states GameStateFrequency, wins GameStateFrequency) GameStateFrequency {
    inProgress := make(GameStateFrequency)
    for state, frequency := range states {
        for _, playerState := range game.stateUpdater(state.p1) {
            newState := GameState{
                p1: state.p2,
                p2: playerState.player,
            }
            newFrequency := playerState.frequency * frequency
            if playerState.player.score >= game.target {
                wins[newState] += newFrequency
            } else {
                inProgress[newState] += newFrequency
            }
        }
    }
    return inProgress
}

type DeterministicDice struct {
    current int
    max int
    moves int
}

func (dice *DeterministicDice) roll() int {
    dice.current %= dice.max
    dice.current++
    dice.moves++
    return dice.current
}

func (dice *DeterministicDice) stateUpdater() func(Player)[]PlayerState {
    return func(player Player) []PlayerState {
        return []PlayerState{
            {
                player: player.move(dice.roll() + dice.roll() + dice.roll()),
                frequency: 1,
            },
        }
    }
}

type QuantumDice struct {
    dimensions int
    rolls int
}

func (dice QuantumDice) stateUpdater() func(Player)[]PlayerState {
    stateSpace := dice.computeStateSpace()
    return func(player Player) []PlayerState {
        var result []PlayerState
        for amount, frequency := range stateSpace {
            playerState := PlayerState{
                player: player.move(amount),
                frequency: frequency,
            }
            result = append(result, playerState)
        }
        return result
    }
}

type StateSpace map[int]int

func (dice QuantumDice) computeStateSpace() StateSpace {
    states := [][]int{
        []int{},
    }
    for i := 1; i <= dice.rolls; i++ {
        newStates := [][]int{}
        for j := 1; j <= dice.dimensions; j++ {
            for _, state := range states {
                newStates = append(newStates, append(state, j))
            }
        }
        states = newStates
    }

    result := make(StateSpace)
    for _, state := range states {
        sum := 0
        for _, value := range state {
            sum += value
        }
        result[sum]++
    }

    return result
}

func main() {
    fmt.Printf("Part 1 = %d \n", part1())
    fmt.Printf("Part 2 = %d \n", part2())
}

func part1() int {
    dice := DeterministicDice{
        current: 0,
        max: 100,
        moves: 0,
    }
    game := Game{
        target: 1000,
        stateUpdater: dice.stateUpdater(),
    }
    gamesWon := game.play(getData())
    result := 0
    for gameWon := range gamesWon {
        if gameWon.p1.score < gameWon.p2.score {
            result += gameWon.p1.score * dice.moves
        } else {
            result += gameWon.p2.score * dice.moves
        }
    }
    return result
}

func part2() int {
    game := Game{
        target: 21,
        stateUpdater: QuantumDice{
            dimensions: 3,
            rolls: 3,
        }.stateUpdater(),
    }
    gamesWon := game.play(getData())
    return gamesWon.total()
}

func getData() (Player, Player) {
    data, _ := ioutil.ReadFile("data.txt")
    players := strings.Split(string(data), "\r\n")
    return parsePlayer(players[0]), parsePlayer(players[1])
}

func parsePlayer(player string) Player {
    rawPosition := strings.Split(player, ": ")[1]
    position, _ := strconv.Atoi(rawPosition)
    return Player{
        position: position,
        score: 0,
    }
}
