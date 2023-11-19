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
	batchSize = 1024
)

type hashSearch struct {
	prefix string
	goal   string
}

func (h hashSearch) runBatch(start int) int {
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
	prefix := strings.TrimSpace(files.Content())
	fiveLeading := firstIndex(prefix, 5, 1)
	answers.Part1(346386, fiveLeading)
	answers.Part2(9958218, firstIndex(prefix, 6, fiveLeading))
}

func firstIndex(prefix string, leadingZeros int, index int) int {
	search := hashSearch{
		prefix: prefix,
		goal:   strings.Repeat("0", leadingZeros),
	}
	for {
		results := make(chan int, batches)
		var wg sync.WaitGroup
		for i := 0; i < batches; i++ {
			wg.Add(1)
			go func(start int) {
				defer wg.Done()
				results <- search.runBatch(start)
			}(index)
			index += batchSize
		}
		wg.Wait()
		close(results)
		for result := range results {
			// Assumes there will not be valid results in multiple batches
			if result != -1 {
				return result
			}
		}
	}
}
