package main

import (
	"advent-of-code/commons/go/answer"
	"advent-of-code/commons/go/file"
	"advent-of-code/commons/go/util"
)

type Player struct {
	position int
	score    int
	moves    int
}

func (player Player) move(amount int) Player {
	newPosition := player.position + amount
	newPosition = ((newPosition - 1) % 10) + 1
	return Player{
		position: newPosition,
		score:    player.score + newPosition,
		moves:    player.moves + 1,
	}
}

type GameState struct {
	p1 Player
	p2 Player
}

func (gameState GameState) losingScore() int {
	return util.Min(gameState.p1.score, gameState.p2.score)
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
	player    Player
	frequency int
}

type Game struct {
	target int
	dice   Dice
}

func (game Game) play(p1, p2 Player) GameStateFrequency {
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
		for _, playerState := range game.dice.roll(state.p1) {
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

type Dice interface {
	roll(Player) []PlayerState
}

type DeterministicDice struct {
	current int
	max     int
	moves   int
}

func (dice *DeterministicDice) roll(player Player) []PlayerState {
	return []PlayerState{
		{
			player:    player.move(dice.next() + dice.next() + dice.next()),
			frequency: 1,
		},
	}
}

func (dice *DeterministicDice) next() int {
	dice.current %= dice.max
	dice.current++
	dice.moves++
	return dice.current
}

type StateSpace map[int]int

type QuantumDice struct {
	dimensions int
	rolls      int
	stateSpace StateSpace
}

func (dice QuantumDice) roll(player Player) []PlayerState {
	var result []PlayerState
	for amount, frequency := range dice.stateSpace {
		playerState := PlayerState{
			player:    player.move(amount),
			frequency: frequency,
		}
		result = append(result, playerState)
	}
	return result
}

func (dice QuantumDice) computeStateSpace() StateSpace {
	states := [][]int{
		{},
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
	answer.Part1(571032, part1())
	answer.Part2(49975322685009, part2())
}

func part1() int {
	dice := DeterministicDice{
		current: 0,
		max:     100,
		moves:   0,
	}
	gamesWon := play(1000, &dice)
	result := 0
	for gameWon := range gamesWon {
		result += gameWon.losingScore() * dice.moves
	}
	return result
}

func part2() int {
	dice := QuantumDice{
		dimensions: 3,
		rolls:      3,
	}
	dice.stateSpace = dice.computeStateSpace()
	gamesWon := play(21, dice)
	return gamesWon.total()
}

func play(target int, dice Dice) GameStateFrequency {
	game := Game{
		target: target,
		dice:   dice,
	}
	return game.play(getPlayers())
}

func getPlayers() (Player, Player) {
	players := file.ReadLines()
	return parsePlayer(players[0]), parsePlayer(players[1])
}

func parsePlayer(player string) Player {
	return Player{
		position: util.ToInt(util.SubstringAfter(player, ": ")),
		score:    0,
	}
}
