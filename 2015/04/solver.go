package main

import (
	"crypto/md5"
	"encoding/hex"
	"strconv"
	"strings"

	"advent-of-code/commons/go/answer"
	"advent-of-code/commons/go/async"
	"advent-of-code/commons/go/file"
)

type hashSearch struct {
	prefix string
	goal   string
}

func (h hashSearch) runBatch(start int, batchSize int) int {
	for i := start; i < start+batchSize; i++ {
		if h.getHash(i)[:len(h.goal)] == h.goal {
			return i
		}
	}
	return -1
}

func (h hashSearch) getHash(i int) string {
	value := h.prefix + strconv.Itoa(i)
	result := md5.Sum([]byte(value))
	return hex.EncodeToString(result[:])
}

func main() {
	answer.Timer(solution)
}

func solution() {
	prefix := file.Default().Content()
	fiveLeading := firstIndex(prefix, 5, 1)
	answer.Part1(346386, fiveLeading)
	answer.Part2(9958218, firstIndex(prefix, 6, fiveLeading))
}

func firstIndex(prefix string, leadingZeros int, index int) int {
	search := hashSearch{
		prefix: prefix,
		goal:   strings.Repeat("0", leadingZeros),
	}
	first := -1
	batch := async.Batch[int]{
		Batches:   8,
		BatchSize: 1024,
		Index:     index,
		Complete: func() bool {
			return first != -1
		},
		Work: search.runBatch,
		ProcessResults: func(results []int) {
			// Assumes there will not be valid results in multiple batches
			for _, result := range results {
				if result != -1 {
					first = result
				}
			}
		},
	}
	batch.Run()
	return first
}
