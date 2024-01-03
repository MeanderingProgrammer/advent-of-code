package main

import (
	"advent-of-code/commons/go/answer"
	"advent-of-code/commons/go/async"
	"advent-of-code/commons/go/file"
	"crypto/md5"
	"encoding/hex"
	"strconv"
	"strings"
)

const (
	offset = 1_000
)

type hashInfo struct {
	index   int
	value   string
	triples []rune
	cinqs   []rune
}

type hashSearch struct {
	prefix string
	hashes int
}

func (h hashSearch) runBatch(start int, batchSize int) []hashInfo {
	result := []hashInfo{}
	for i := start; i < start+batchSize; i++ {
		result = append(result, h.getHash(i))
	}
	return result
}

func (h hashSearch) getHash(index int) hashInfo {
	value := h.prefix + strconv.Itoa(index)
	for i := 0; i < h.hashes; i++ {
		result := md5.Sum([]byte(value))
		value = hex.EncodeToString(result[:])
	}
	return hashInfo{index: index, triples: getRepeats(value, 3), cinqs: getRepeats(value, 5)}
}

func getRepeats(value string, length int) []rune {
	repeats := []rune{}
	for i := 0; i <= len(value)-length; i++ {
		subString := value[i : i+length]
		if sameChar(subString) {
			repeats = append(repeats, rune(subString[0]))
		}
	}
	return repeats
}

func sameChar(value string) bool {
	firstChar := rune(value[0])
	for _, char := range value[1:] {
		if char != firstChar {
			return false
		}
	}
	return true
}

func main() {
	prefix := strings.TrimSpace(file.Content())
	answer.Part1(15168, generate(hashSearch{prefix: prefix, hashes: 1}))
	answer.Part2(20864, generate(hashSearch{prefix: prefix, hashes: 2_017}))
}

func generate(search hashSearch) int {
	infos := make(map[int]hashInfo)
	index := 0
	keys := []int{}
	batch := async.Batch[[]hashInfo]{
		Batches:   8,
		BatchSize: 64,
		Index:     0,
		Complete: func() bool {
			return len(keys) >= 64
		},
		Work: search.runBatch,
		ProcessResults: func(results [][]hashInfo) {
			for _, result := range results {
				for _, info := range result {
					infos[info.index] = info
				}
			}
			for index < len(infos)-offset {
				info := infos[index]
				if len(info.triples) > 0 && contains(infos, index+1, info.triples[0]) {
					keys = append(keys, index)
				}
				index++
			}
		},
	}
	batch.Run()
	return keys[63]
}

func contains(infos map[int]hashInfo, index int, target rune) bool {
	for i := index; i < index+offset; i++ {
		for _, value := range infos[i].cinqs {
			if value == target {
				return true
			}
		}
	}
	return false
}
