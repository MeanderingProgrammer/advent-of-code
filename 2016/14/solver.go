package main

import (
	"advent-of-code/commons/go/answers"
	"advent-of-code/commons/go/files"
	"crypto/md5"
	"encoding/hex"
	"strconv"
	"strings"
	"sync"
)

const (
	batches   = 8
	batchSize = 64
	offset    = 1_000
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

func (h hashSearch) runBatch(start int) []hashInfo {
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
	prefix := strings.TrimSpace(files.Content())
	answers.Part1(15168, generate(hashSearch{prefix: prefix, hashes: 1}))
	answers.Part2(20864, generate(hashSearch{prefix: prefix, hashes: 2_017}))
}

func generate(search hashSearch) int {
	infos := make(map[int]hashInfo)
	index, keys := 0, []int{}
	for len(keys) < 64 {
		addBatch(search, infos)
		for index < len(infos)-offset {
			info := infos[index]
			if len(info.triples) > 0 && contains(infos, index+1, info.triples[0]) {
				keys = append(keys, index)
			}
			index++
		}
	}
	return keys[63]
}

func addBatch(search hashSearch, infos map[int]hashInfo) {
	results := make(chan hashInfo, batches*batchSize)
	var wg sync.WaitGroup
	for i := 0; i < batches; i++ {
		wg.Add(1)
		go func(start int) {
			defer wg.Done()
			for _, value := range search.runBatch(start) {
				results <- value
			}
		}(len(infos) + (i * batchSize))
	}
	wg.Wait()
	close(results)
	for result := range results {
		infos[result.index] = result
	}
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
