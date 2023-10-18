package main

import (
	"advent-of-code/commons/go/answers"
	"advent-of-code/commons/go/files"
	"crypto/md5"
	"encoding/hex"
	"strconv"
)

type Part struct {
	part   int
	result string
}

type Populator interface {
	populate(passwords map[int]string, hash string)
}

type Part1 struct{}

func (p *Part1) populate(passwords map[int]string, hash string) {
	passwords[len(passwords)] = string(hash[5])
}

type Part2 struct{}

func (p *Part2) populate(passwords map[int]string, hash string) {
	index, err := strconv.Atoi(string(hash[5]))
	if err != nil || index > 7 {
		return
	}
	_, ok := passwords[index]
	if ok {
		return
	}
	passwords[index] = string(hash[6])
}

func main() {
	doorId := files.Content()
	parts := make(chan Part)
	solvePart := func(part int, populator Populator) {
		parts <- Part{
			part:   part,
			result: getPassword(doorId, populator),
		}
	}
	go solvePart(1, &Part1{})
	go solvePart(2, &Part2{})
	res1, res2 := <-parts, <-parts
	if res2.part == 1 {
		res1, res2 = res2, res1
	}
	answers.Part1("d4cd2ee1", res1.result)
	answers.Part2("f2c730e5", res2.result)
}

func getPassword(doorId string, populator Populator) string {
	index := 0
	passwords := make(map[int]string)
	for len(passwords) < 8 {
		hash := getHash(doorId, index)
		if hash[0:5] == "00000" {
			populator.populate(passwords, hash)
		}
		index++
	}
	result := ""
	for i := 0; i < len(passwords); i++ {
		value, _ := passwords[i]
		result += value
	}
	return result
}

func getHash(doorId string, index int) string {
	value := doorId + strconv.Itoa(index)
	hasher := md5.New()
	hasher.Write([]byte(value))
	return hex.EncodeToString(hasher.Sum(nil))
}
