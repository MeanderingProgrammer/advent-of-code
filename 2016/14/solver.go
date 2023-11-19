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
		value := h.getHash(i)
		if len(value.triples) > 0 {
			result = append(result, value)
		}
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
	for i := 0; i < offset; i++ {
		value := search.getHash(i)
		if len(value.triples) > 0 {
			infos[i] = value
		}
	}

	index := 0
	keys := []int{}
	var mu sync.Mutex
	for len(keys) < 64 {
		var wg sync.WaitGroup
		for i := 0; i < batches; i++ {
			wg.Add(1)
			go func(start int) {
				defer wg.Done()
				for _, value := range search.runBatch(start) {
					mu.Lock()
					infos[value.index] = value
					mu.Unlock()
				}
			}(offset + index + (i * batchSize))
		}
		wg.Wait()

		end := index + (batches * batchSize)
		for index < end {
			info, ok := infos[index]
			if ok {
				if contains(infos, index+1, info.triples[0]) {
					keys = append(keys, index)
				}
			}
			index++
		}
	}
	return keys[63]
}

func contains(infos map[int]hashInfo, index int, target rune) bool {
	for i := index; i < index+offset; i++ {
		info, ok := infos[i]
		if ok {
			for _, value := range info.cinqs {
				if value == target {
					return true
				}
			}
		}
	}
	return false
}
