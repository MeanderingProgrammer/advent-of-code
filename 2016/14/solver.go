package main

import (
	"advent-of-code/commons/go/answers"
	"crypto/md5"
	"encoding/hex"
	"github.com/gammazero/deque"
	"strconv"
)

type hashInfo struct {
	value string
	cinqs []rune
}

func main() {
	answers.Part1(15168, generate(64, 1))
	answers.Part2(20864, generate(64, 2_017))
}

func generate(n int, hashes int) int {
	index := 0
	infos := deque.New[hashInfo]()
	for index < 1_000 {
		infos.PushBack(getHash(index, hashes))
		index++
	}

	keys := []int{}
	for len(keys) < n {
		info := infos.PopFront()
		infos.PushBack(getHash(index, hashes))
		triples := getRepeats(info.value, 3)
		if len(triples) > 0 {
			if contains(infos, triples[0]) {
				keys = append(keys, index-infos.Len())
			}
		}
		index++
	}
	return keys[len(keys)-1]
}

func getHash(index int, hashes int) hashInfo {
	value := "qzyelonm" + strconv.Itoa(index)
	for i := 0; i < hashes; i++ {
		hasher := md5.New()
		hasher.Write([]byte(value))
		value = hex.EncodeToString(hasher.Sum(nil))
	}
	return hashInfo{value: value, cinqs: getRepeats(value, 5)}
}

func getRepeats(value string, length int) []rune {
	repeats := []rune{}
	for i := 0; i <= len(value)-length; i++ {
		subString := value[i : i+length]
		repeat := sameRune(subString)
		if repeat != nil {
			repeats = append(repeats, *repeat)
		}
	}
	return repeats
}

func sameRune(value string) *rune {
	runes := []rune(value)
	firstRune := runes[0]
	for i := 1; i < len(value); i++ {
		if runes[i] != firstRune {
			return nil
		}
	}
	return &firstRune
}

func contains(infos *deque.Deque[hashInfo], target rune) bool {
	for i := 0; i < infos.Len(); i++ {
		info := infos.At(i)
		for _, value := range info.cinqs {
			if value == target {
				return true
			}
		}
	}
	return false
}
